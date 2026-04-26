"""
员工个人知识库管理模块
支持 Obsidian Vault 同步和个人知识图谱构建
"""
import os
import json
import uuid
import logging
import time
import hashlib
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from sqlalchemy import select, and_, or_

from database import get_db_session, get_engine, Base
from database import ObsidianVaultModel, PersonalKnowledgeGraphModel, KnowledgeRelationModel
from database import PersonalNoteModel, PersonalMemoryModel

logger = logging.getLogger(__name__)


class ObsidianVaultManager:
    """Obsidian Vault 管理器"""

    def __init__(self):
        pass  # 表已在 database.py 中定义

    def create_vault(
        self,
        employee_id: str,
        vault_path: str,
        vault_name: str = "",
        vault_url: str = "",
        access_token: str = "",
    ) -> ObsidianVaultModel:
        """创建 Obsidian Vault 配置"""
        with get_db_session() as session:
            vault_id = str(uuid.uuid4())
            now = datetime.now()
            vault = ObsidianVaultModel(
                id=vault_id,
                employee_id=employee_id,
                vault_path=vault_path,
                vault_name=vault_name or os.path.basename(vault_path),
                vault_url=vault_url,
                access_token=access_token,
                created_at=now,
                updated_at=now,
            )
            session.add(vault)
            session.flush()
            session.expunge(vault)
            return vault

    def get_by_employee(self, employee_id: str) -> List[ObsidianVaultModel]:
        """获取员工的所有 Vault"""
        with get_db_session() as session:
            stmt = select(ObsidianVaultModel).where(
                and_(
                    ObsidianVaultModel.employee_id == employee_id,
                    ObsidianVaultModel.is_active == True,
                )
            )
            results = session.execute(stmt).scalars().all()
            for r in results:
                session.expunge(r)
            return list(results)

    def update_last_sync(self, vault_id: str):
        """更新最后同步时间"""
        import time
        with get_db_session() as session:
            stmt = select(ObsidianVaultModel).where(ObsidianVaultModel.id == vault_id)
            vault = session.execute(stmt).scalar_one_or_none()
            if vault:
                vault.last_sync_at = time.time()
                vault.updated_at = datetime.now()


class ObsidianSyncer:
    """Obsidian Vault 同步器"""

    def __init__(self, vault_config: ObsidianVaultModel):
        self.vault_config = vault_config
        self.vault_path = Path(vault_config.vault_path)

    def sync(self) -> Dict[str, Any]:
        """同步 Vault 到数据库"""
        if not self.vault_path.exists():
            return {"status": "error", "message": f"Vault path not found: {self.vault_path}"}

        manager = PersonalNoteManager()
        notes_added = 0
        notes_updated = 0

        for ext in self.vault_config.file_extensions:
            for md_file in self.vault_path.rglob(f"*{ext}"):
                if self._should_exclude(md_file):
                    continue

                try:
                    result = self._process_note(md_file)
                    if result == "added":
                        notes_added += 1
                    elif result == "updated":
                        notes_updated += 1
                except Exception as e:
                    logger.error(f"Failed to process {md_file}: {e}")

        return {
            "status": "success",
            "notes_added": notes_added,
            "notes_updated": notes_updated,
        }

    def _should_exclude(self, file_path: Path) -> bool:
        """检查是否应该排除该文件"""
        exclude_folders = self.vault_config.exclude_folders or []
        for folder in exclude_folders:
            if folder in file_path.parts:
                return True
        return False

    def _process_note(self, file_path: Path) -> str:
        """处理单个笔记文件"""
        import hashlib
        import frontmatter

        content = file_path.read_text(encoding="utf-8")
        content_hash = hashlib.md5(content.encode()).hexdigest()

        try:
            post = frontmatter.loads(content)
            frontmatter_data = dict(post.metadata)
            text_content = post.content.strip()
        except:
            text_content = content
            frontmatter_data = {}

        title = frontmatter_data.get("title", file_path.stem)
        tags = frontmatter_data.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]

        links = self._extract_links(text_content)
        word_count = len(text_content)

        manager = PersonalNoteManager()
        return manager.upsert_note(
            employee_id=self.vault_config.employee_id,
            vault_id=self.vault_config.id,
            file_path=str(file_path),
            file_name=file_path.name,
            title=title,
            content=text_content,
            tags=tags,
            links=links,
            frontmatter=frontmatter_data,
            word_count=word_count,
            content_hash=content_hash,
            last_modified=file_path.stat().st_mtime,
        )

    def _extract_links(self, content: str) -> List[str]:
        """提取笔记中的链接"""
        import re
        wiki_links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
        md_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        return wiki_links + [link[1] for link in md_links if link[1].endswith('.md')]


class PersonalNoteManager:
    """个人笔记管理器"""

    def upsert_note(
        self,
        employee_id: str,
        file_path: str,
        file_name: str,
        title: str,
        content: str,
        vault_id: str = None,
        tags: List[str] = None,
        links: List[str] = None,
        frontmatter: Dict = None,
        word_count: int = 0,
        content_hash: str = "",
        last_modified: float = 0,
    ) -> str:
        """插入或更新笔记"""
        with get_db_session() as session:
            stmt = select(PersonalNoteModel).where(
                and_(
                    PersonalNoteModel.employee_id == employee_id,
                    PersonalNoteModel.file_path == file_path,
                )
            )
            existing = session.execute(stmt).scalar_one_or_none()

            now = datetime.now()
            if existing:
                if existing.hash_content == content_hash:
                    return "unchanged"
                existing.title = title
                existing.content = content
                existing.tags = tags or []
                existing.links = links or []
                existing.frontmatter_json = frontmatter or {}
                existing.word_count = word_count
                existing.hash_content = content_hash
                existing.last_modified = last_modified
                existing.is_processed = False
                existing.updated_at = now
                result = "updated"
            else:
                note = PersonalNoteModel(
                    id=str(uuid.uuid4()),
                    employee_id=employee_id,
                    vault_id=vault_id,
                    file_path=file_path,
                    file_name=file_name,
                    title=title,
                    content=content,
                    tags=tags or [],
                    links=links or [],
                    frontmatter_json=frontmatter or {},
                    word_count=word_count,
                    hash_content=content_hash,
                    last_modified=last_modified,
                    created_at=now,
                    updated_at=now,
                )
                session.add(note)
                result = "added"

            session.flush()
            return result

    def get_notes_for_embedding(self, employee_id: str, limit: int = 100) -> List[PersonalNoteModel]:
        """获取待嵌入的笔记"""
        with get_db_session() as session:
            stmt = select(PersonalNoteModel).where(
                and_(
                    PersonalNoteModel.employee_id == employee_id,
                    PersonalNoteModel.is_processed == False,
                )
            ).limit(limit)
            return list(session.execute(stmt).scalars().all())

    def mark_processed(self, note_id: str, embedding_id: str):
        """标记笔记已处理"""
        with get_db_session() as session:
            stmt = select(PersonalNoteModel).where(PersonalNoteModel.id == note_id)
            note = session.execute(stmt).scalar_one_or_none()
            if note:
                note.is_processed = True
                note.embedding_vector_id = embedding_id


class KnowledgeGraphExtractor:
    """从笔记中提取知识图谱"""

    def __init__(self, employee_id: str):
        self.employee_id = employee_id

    def extract_from_notes(self, notes: List[PersonalNoteModel]) -> Dict[str, Any]:
        """从笔记列表中提取知识图谱"""
        entities_added = 0
        relations_added = 0

        for note in notes:
            result = self._extract_from_note(note)
            entities_added += result["entities"]
            relations_added += result["relations"]

        return {
            "entities_added": entities_added,
            "relations_added": relations_added,
        }

    def _extract_from_note(self, note: PersonalNoteModel) -> Dict[str, int]:
        """从单个笔记提取"""
        import re

        entities = []
        relations = []

        tags = note.tags or []
        for tag in tags:
            entities.append({
                "type": "tag",
                "name": tag,
                "source_note": note.file_name,
            })

        wiki_links = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', note.content)
        for link in wiki_links:
            target = link[0]
            alias = link[1] if len(link) > 1 else None
            relations.append({
                "from": note.title,
                "to": target,
                "type": "links_to",
                "label": alias or target,
            })
            entities.append({
                "type": "concept",
                "name": target,
                "source_note": note.file_name,
            })

        entity_manager = KnowledgeGraphManager()
        entities_added = entity_manager.add_entities(self.employee_id, entities)
        relations_added = entity_manager.add_relations(self.employee_id, relations)

        return {"entities": entities_added, "relations": relations_added}


class KnowledgeGraphManager:
    """知识图谱管理器"""

    def add_entities(self, employee_id: str, entities: List[Dict]) -> int:
        """添加实体"""
        added = 0
        with get_db_session() as session:
            for entity in entities:
                stmt = select(PersonalKnowledgeGraphModel).where(
                    and_(
                        PersonalKnowledgeGraphModel.employee_id == employee_id,
                        PersonalKnowledgeGraphModel.entity_name == entity.get("name"),
                    )
                )
                existing = session.execute(stmt).scalar_one_or_none()
                if not existing:
                    now = datetime.now()
                    ent = PersonalKnowledgeGraphModel(
                        id=str(uuid.uuid4()),
                        employee_id=employee_id,
                        entity_type=entity.get("type", "concept"),
                        entity_name=entity.get("name"),
                        entity_aliases=[],
                        description=entity.get("description", ""),
                        source_note=entity.get("source_note", ""),
                        tags=entity.get("tags", []),
                        created_at=now,
                        updated_at=now,
                    )
                    session.add(ent)
                    added += 1
            session.flush()
        return added

    def add_relations(self, employee_id: str, relations: List[Dict]) -> int:
        """添加关系"""
        import hashlib
        added = 0
        with get_db_session() as session:
            for rel in relations:
                from_name = rel.get("from", "")
                to_name = rel.get("to", "")

                if not from_name or not to_name:
                    continue

                stmt_from = select(PersonalKnowledgeGraphModel).where(
                    and_(
                        PersonalKnowledgeGraphModel.employee_id == employee_id,
                        PersonalKnowledgeGraphModel.entity_name == from_name,
                    )
                )
                from_entity = session.execute(stmt_from).scalar_one_or_none()

                stmt_to = select(PersonalKnowledgeGraphModel).where(
                    and_(
                        PersonalKnowledgeGraphModel.employee_id == employee_id,
                        PersonalKnowledgeGraphModel.entity_name == to_name,
                    )
                )
                to_entity = session.execute(stmt_to).scalar_one_or_none()

                if from_entity and to_entity:
                    rel_hash = hashlib.md5(
                        f"{from_entity.id}{to_entity.id}{rel.get('type')}".encode()
                    ).hexdigest()[:16]

                    stmt_rel = select(KnowledgeRelationModel).where(
                        and_(
                            KnowledgeRelationModel.employee_id == employee_id,
                            KnowledgeRelationModel.from_entity_id == from_entity.id,
                            KnowledgeRelationModel.to_entity_id == to_entity.id,
                        )
                    )
                    existing = session.execute(stmt_rel).scalar_one_or_none()

                    if not existing:
                        now = datetime.now()
                        relation = KnowledgeRelationModel(
                            id=str(uuid.uuid4()),
                            employee_id=employee_id,
                            from_entity_id=from_entity.id,
                            to_entity_id=to_entity.id,
                            relation_type=rel.get("type", "related_to"),
                            relation_label=rel.get("label", ""),
                            source_note=rel.get("source_note", ""),
                            created_at=now,
                            updated_at=now,
                        )
                        session.add(relation)
                        added += 1
            session.flush()
        return added

    def get_related_entities(
        self,
        employee_id: str,
        entity_name: str,
        depth: int = 2,
    ) -> List[Dict]:
        """获取关联实体（支持多跳）"""
        with get_db_session() as session:
            stmt = select(PersonalKnowledgeGraphModel).where(
                and_(
                    PersonalKnowledgeGraphModel.employee_id == employee_id,
                    PersonalKnowledgeGraphModel.entity_name == entity_name,
                )
            )
            entity = session.execute(stmt).scalar_one_or_none()
            if not entity:
                return []

            visited = {entity.id}
            result = [self._entity_to_dict(entity)]

            current_ids = [entity.id]
            for _ in range(depth):
                next_ids = []
                for eid in current_ids:
                    stmt_rels = select(KnowledgeRelationModel).where(
                        or_(
                            KnowledgeRelationModel.from_entity_id == eid,
                            KnowledgeRelationModel.to_entity_id == eid,
                        )
                    )
                    rels = session.execute(stmt_rels).scalars().all()

                    for rel in rels:
                        neighbor_id = (
                            rel.to_entity_id
                            if rel.from_entity_id == eid
                            else rel.from_entity_id
                        )
                        if neighbor_id not in visited:
                            visited.add(neighbor_id)
                            stmt_neighbor = select(PersonalKnowledgeGraphModel).where(
                                PersonalKnowledgeGraphModel.id == neighbor_id
                            )
                            neighbor = session.execute(stmt_neighbor).scalar_one_or_none()
                            if neighbor:
                                result.append(self._entity_to_dict(neighbor))
                                next_ids.append(neighbor_id)

                current_ids = next_ids
                if not current_ids:
                    break

            return result

    def _entity_to_dict(self, entity: PersonalKnowledgeGraphModel) -> Dict:
        return {
            "id": entity.id,
            "name": entity.entity_name,
            "type": entity.entity_type,
            "description": entity.description,
            "tags": entity.tags or [],
            "importance": entity.importance_score,
        }


class PersonalMemoryManager:
    """个人记忆管理器 - 存储 AI 对员工的理解"""

    def __init__(self, employee_id: str):
        self.employee_id = employee_id

    def add_memory(
        self,
        memory_type: str,
        memory_key: str,
        content: str,
        summary: str = "",
        confidence: float = 0.8,
        source_messages: List[str] = None,
    ) -> PersonalMemoryModel:
        """添加个人记忆"""
        import time
        with get_db_session() as session:
            stmt = select(PersonalMemoryModel).where(
                and_(
                    PersonalMemoryModel.employee_id == self.employee_id,
                    PersonalMemoryModel.memory_key == memory_key,
                )
            )
            existing = session.execute(stmt).scalar_one_or_none()

            now = datetime.now()
            if existing:
                existing.memory_content = content
                existing.memory_summary = summary
                existing.confidence = confidence
                existing.source_messages = source_messages or []
                existing.updated_at = now
                existing.access_count += 1
                memory = existing
            else:
                memory = PersonalMemoryModel(
                    id=str(uuid.uuid4()),
                    employee_id=self.employee_id,
                    memory_type=memory_type,
                    memory_key=memory_key,
                    memory_content=content,
                    memory_summary=summary,
                    confidence=confidence,
                    source_messages=source_messages or [],
                    created_at=now,
                    updated_at=now,
                )
                session.add(memory)

            session.flush()
            session.expunge(memory)
            return memory

    def get_memories(
        self,
        memory_type: str = None,
        min_confidence: float = 0.5,
    ) -> List[Dict]:
        """获取个人记忆"""
        with get_db_session() as session:
            query = select(PersonalMemoryModel).where(
                and_(
                    PersonalMemoryModel.employee_id == self.employee_id,
                    PersonalMemoryModel.confidence >= min_confidence,
                )
            )
            if memory_type:
                query = query.where(PersonalMemoryModel.memory_type == memory_type)

            query = query.order_by(PersonalMemoryModel.confidence.desc())
            results = session.execute(query).scalars().all()

            memories = []
            for r in results:
                memories.append({
                    "type": r.memory_type,
                    "key": r.memory_key,
                    "content": r.memory_content,
                    "summary": r.memory_summary,
                    "confidence": r.confidence,
                })
            return memories

    def build_memory_context(self) -> str:
        """构建记忆上下文"""
        memories = self.get_memories(min_confidence=0.6)
        if not memories:
            return ""

        context_parts = ["\n## 关于这个用户的信息："]
        current_type = None
        for m in memories:
            if m["type"] != current_type:
                context_parts.append(f"\n### {m['type']}:")
                current_type = m["type"]
            context_parts.append(f"- {m['summary'] or m['content'][:100]}")

        return "\n".join(context_parts)


def init_obsidian_tables():
    """初始化 Obsidian 相关表"""
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine, tables=[
            ObsidianVaultModel.__table__,
            PersonalKnowledgeGraphModel.__table__,
            KnowledgeRelationModel.__table__,
            PersonalNoteModel.__table__,
            PersonalMemoryModel.__table__,
        ])
        logger.info("Obsidian tables initialized")
    except Exception as e:
        logger.warning(f"Failed to init obsidian tables: {e}")
