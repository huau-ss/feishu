"""
个人知识库 API - 支持飞书端直接上传笔记
员工可以在飞书端直接创建/上传笔记，无需 Obsidian
"""
import uuid
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from sqlalchemy import select, and_

from database import get_db_session, PersonalNoteModel, PersonalMemoryModel, ObsidianVaultModel
from core.personal_knowledge import KnowledgeGraphExtractor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/personal-kb", tags=["个人知识库"])


@router.get("/notes")
async def get_notes(
    employee_id: str,
    vault_id: str = None,
    tag: str = None,
    search: str = None,
    limit: int = 50,
):
    """获取员工的个人笔记"""
    with get_db_session() as session:
        stmt = select(PersonalNoteModel).where(
            PersonalNoteModel.employee_id == employee_id
        )

        if vault_id:
            stmt = stmt.where(PersonalNoteModel.vault_id == vault_id)

        if tag:
            stmt = stmt.where(PersonalNoteModel.tags.contains([tag]))

        if search:
            stmt = stmt.where(PersonalNoteModel.content.contains(search))

        stmt = stmt.order_by(PersonalNoteModel.updated_at.desc()).limit(limit)
        notes = session.execute(stmt).scalars().all()

        return {
            "notes": [
                {
                    "id": n.id,
                    "title": n.title,
                    "file_name": n.file_name,
                    "content": n.content[:500],  # 预览前500字
                    "tags": n.tags or [],
                    "word_count": n.word_count,
                    "updated_at": n.updated_at,
                }
                for n in notes
            ]
        }


@router.post("/notes")
async def create_note(
    employee_id: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    tags: str = Form("[]"),  # JSON string
    vault_id: str = Form(None),
):
    """创建个人笔记（飞书端直接创建）"""
    import json
    import hashlib

    try:
        tag_list = json.loads(tags) if tags else []
    except:
        tag_list = []

    content_hash = hashlib.md5(content.encode()).hexdigest()

    with get_db_session() as session:
        now = datetime.now()
        note = PersonalNoteModel(
            id=str(uuid.uuid4()),
            employee_id=employee_id,
            vault_id=vault_id,
            file_path=f"personal/{employee_id}/{title}.md",
            file_name=f"{title}.md",
            title=title,
            content=content,
            tags=tag_list,
            word_count=len(content),
            hash_content=content_hash,
            last_modified=now.timestamp(),
            created_at=now,
            updated_at=now,
        )
        session.add(note)
        session.flush()

        note_id = note.id

    # 提取知识图谱
    try:
        extractor = KnowledgeGraphExtractor(employee_id)
        with get_db_session() as session:
            note_model = session.query(PersonalNoteModel).filter_by(id=note_id).first()
            if note_model:
                session.expunge(note_model)
                extractor.extract_from_notes([note_model])
    except Exception as e:
        logger.warning(f"Failed to extract knowledge graph: {e}")

    return {"success": True, "id": note_id}


@router.put("/notes/{note_id}")
async def update_note(
    note_id: str,
    title: str = Form(None),
    content: str = Form(None),
    tags: str = Form(None),
):
    """更新个人笔记"""
    import json
    import hashlib

    with get_db_session() as session:
        stmt = select(PersonalNoteModel).where(PersonalNoteModel.id == note_id)
        note = session.execute(stmt).scalar_one_or_none()

        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        if title is not None:
            note.title = title
            note.file_name = f"{title}.md"

        if content is not None:
            note.content = content
            note.word_count = len(content)
            note.hash_content = hashlib.md5(content.encode()).hexdigest()
            note.is_processed = False  # 重新处理

        if tags is not None:
            try:
                note.tags = json.loads(tags)
            except:
                pass

        note.updated_at = datetime.now()

    return {"success": True}


@router.delete("/notes/{note_id}")
async def delete_note(note_id: str):
    """删除个人笔记"""
    with get_db_session() as session:
        stmt = select(PersonalNoteModel).where(PersonalNoteModel.id == note_id)
        note = session.execute(stmt).scalar_one_or_none()

        if not note:
            raise HTTPException(status_code=404, detail="Note not found")

        session.delete(note)

    return {"success": True}


@router.post("/notes/batch")
async def batch_create_notes(
    employee_id: str = Form(...),
    notes_json: str = Form(...),  # JSON array of {title, content, tags}
):
    """批量创建笔记"""
    import json

    try:
        notes_data = json.loads(notes_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    created_ids = []
    now = datetime.now()

    with get_db_session() as session:
        for note_data in notes_data:
            note = PersonalNoteModel(
                id=str(uuid.uuid4()),
                employee_id=employee_id,
                file_path=f"personal/{employee_id}/{note_data.get('title', 'untitled')}.md",
                file_name=f"{note_data.get('title', 'untitled')}.md",
                title=note_data.get("title", "untitled"),
                content=note_data.get("content", ""),
                tags=note_data.get("tags", []),
                word_count=len(note_data.get("content", "")),
                last_modified=now.timestamp(),
                created_at=now,
                updated_at=now,
            )
            session.add(note)
            created_ids.append(note.id)

    return {"success": True, "created": len(created_ids), "ids": created_ids}


@router.get("/memories")
async def get_memories(
    employee_id: str,
    memory_type: str = None,
    min_confidence: float = 0.5,
):
    """获取个人记忆"""
    with get_db_session() as session:
        query = select(PersonalMemoryModel).where(
            and_(
                PersonalMemoryModel.employee_id == employee_id,
                PersonalMemoryModel.confidence >= min_confidence,
            )
        )

        if memory_type:
            query = query.where(PersonalMemoryModel.memory_type == memory_type)

        query = query.order_by(PersonalMemoryModel.confidence.desc())
        results = session.execute(query).scalars().all()

        return {
            "memories": [
                {
                    "id": m.id,
                    "type": m.memory_type,
                    "key": m.memory_key,
                    "content": m.memory_content,
                    "summary": m.memory_summary,
                    "confidence": m.confidence,
                    "created_at": m.created_at,
                }
                for m in results
            ]
        }


@router.post("/memories")
async def create_memory(
    employee_id: str = Form(...),
    memory_type: str = Form("preference"),
    memory_key: str = Form(...),
    content: str = Form(...),
    summary: str = Form(""),
    confidence: float = Form(0.8),
):
    """创建个人记忆"""
    now = datetime.now()
    with get_db_session() as session:
        stmt = select(PersonalMemoryModel).where(
            and_(
                PersonalMemoryModel.employee_id == employee_id,
                PersonalMemoryModel.memory_key == memory_key,
            )
        )
        existing = session.execute(stmt).scalar_one_or_none()

        if existing:
            existing.memory_content = content
            existing.memory_summary = summary
            existing.confidence = confidence
            existing.updated_at = now
            existing.access_count += 1
            memory_id = existing.id
        else:
            memory = PersonalMemoryModel(
                id=str(uuid.uuid4()),
                employee_id=employee_id,
                memory_type=memory_type,
                memory_key=memory_key,
                memory_content=content,
                memory_summary=summary,
                confidence=confidence,
                created_at=now,
                updated_at=now,
            )
            session.add(memory)
            memory_id = memory.id

    return {"success": True, "id": memory_id}


@router.get("/knowledge-graph")
async def get_knowledge_graph(
    employee_id: str,
    entity_name: str = None,
    depth: int = 2,
):
    """获取知识图谱"""
    try:
        from core.personal_knowledge import KnowledgeGraphManager

        if entity_name:
            manager = KnowledgeGraphManager(employee_id)
            entities = manager.get_related_entities(employee_id, entity_name, depth=depth)
            return {"entities": entities, "type": "related"}
        else:
            from database import PersonalKnowledgeGraphModel
            stmt = select(PersonalKnowledgeGraphModel).where(
                PersonalKnowledgeGraphModel.employee_id == employee_id
            ).order_by(
                PersonalKnowledgeGraphModel.importance_score.desc()
            ).limit(100)

            with get_db_session() as session:
                entities = session.execute(stmt).scalars().all()
                return {
                    "entities": [
                        {
                            "id": e.id,
                            "name": e.entity_name,
                            "type": e.entity_type,
                            "description": e.description,
                            "tags": e.tags or [],
                            "importance": e.importance_score,
                        }
                        for e in entities
                    ],
                    "type": "all",
                }
    except Exception as e:
        logger.error(f"Failed to get knowledge graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn")
async def learn_from_text(
    employee_id: str = Form(...),
    text: str = Form(...),
    context: str = Form(""),
):
    """从文本中学习 - AI 自动提取关键信息"""
    try:
        from core.personal_rag import CyberEmployeeBuilder

        builder = CyberEmployeeBuilder(employee_id)

        # 从文本中提取实体并学习
        entities = builder._extract_entities(text)

        memories_created = 0
        for entity in entities:
            try:
                from core.personal_knowledge import PersonalMemoryManager
                manager = PersonalMemoryManager(employee_id)
                manager.add_memory(
                    memory_type="interest",
                    memory_key=f"mentioned_{entity}",
                    content=f"对话中提到: {entity}",
                    summary=f"用户关注: {entity}",
                    confidence=0.6,
                    source_messages=[text[:200]],
                )
                memories_created += 1
            except:
                pass

        return {
            "success": True,
            "entities_found": len(entities),
            "memories_created": memories_created,
        }
    except Exception as e:
        logger.error(f"Failed to learn: {e}")
        raise HTTPException(status_code=500, detail=str(e))
