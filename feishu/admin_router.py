"""
飞书 Bot 管理后台 API 路由
提供 Skill 和员工管理接口
"""

import logging
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Query

from feishu.employee_manager import (
    EmployeeManager,
    SkillManager,
    FeishuSessionManager,
    get_employee_manager,
    get_skill_manager,
    get_feishu_session_manager,
)
from database import get_db_session, FeishuSessionModel
from sqlalchemy import select, func

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["管理后台"])


class SkillCreateRequest(Dict):
    pass


@router.get("/skills")
async def list_skills():
    """获取所有 Skill 模板"""
    manager = get_skill_manager()
    skills = manager.list_all(include_inactive=True)
    return {
        "skills": [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "answer_style": s.answer_style,
                "temperature": s.temperature,
                "max_tokens": s.max_tokens,
                "knowledge_scope": s.knowledge_scope,
                "priority": s.priority,
                "is_active": s.is_active,
                "created_at": str(s.created_at) if s.created_at else "",
                "updated_at": str(s.updated_at) if s.updated_at else "",
                "system_prompt_suffix": s.system_prompt_suffix,
            }
            for s in skills
        ]
    }


@router.post("/skills")
async def create_skill(request: Dict[str, Any]):
    """创建新 Skill"""
    manager = get_skill_manager()
    try:
        skill = manager.create(
            name=request.get("name", "新 Skill"),
            description=request.get("description", ""),
            system_prompt_suffix=request.get("system_prompt_suffix", ""),
            answer_style=request.get("answer_style", "balanced"),
            temperature=float(request.get("temperature", 0.7)),
            max_tokens=int(request.get("max_tokens", 2048)),
            knowledge_scope=request.get("knowledge_scope", []),
            priority=int(request.get("priority", 0)),
        )
        return {"success": True, "id": skill.id}
    except Exception as e:
        logger.error(f"Failed to create skill: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/skills/{skill_id}")
async def update_skill(skill_id: str, request: Dict[str, Any]):
    """更新 Skill"""
    manager = get_skill_manager()
    fields = {}
    if "name" in request:
        fields["name"] = request["name"]
    if "description" in request:
        fields["description"] = request["description"]
    if "answer_style" in request:
        fields["answer_style"] = request["answer_style"]
    if "temperature" in request:
        fields["temperature"] = float(request["temperature"])
    if "max_tokens" in request:
        fields["max_tokens"] = int(request["max_tokens"])
    if "knowledge_scope" in request:
        fields["knowledge_scope"] = request["knowledge_scope"]
    if "priority" in request:
        fields["priority"] = int(request["priority"])
    if "system_prompt_suffix" in request:
        fields["system_prompt_suffix"] = request["system_prompt_suffix"]
    if "is_active" in request:
        fields["is_active"] = bool(request["is_active"])

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    success = manager.update(skill_id, **fields)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"success": True}


@router.delete("/skills/{skill_id}")
async def delete_skill(skill_id: str):
    """删除 Skill（软删除）"""
    manager = get_skill_manager()
    if skill_id in ("skill_default", "skill_rigorous", "skill_efficient", "skill_beginner"):
        raise HTTPException(status_code=403, detail="Cannot delete built-in skills")
    success = manager.delete(skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"success": True}


@router.get("/employees")
async def list_employees():
    """获取所有员工"""
    manager = get_employee_manager()
    employees = manager.list_all(include_inactive=True)
    skill_manager = get_skill_manager()

    result = []
    for emp in employees:
        skill = skill_manager.get_by_id(emp.skill_id) if emp.skill_id else None
        result.append({
            "id": emp.id,
            "feishu_user_id": emp.feishu_user_id,
            "name": emp.name,
            "department": emp.department,
            "skill_id": emp.skill_id,
            "skill_name": skill.name if skill else None,
            "is_active": emp.is_active,
            "email": emp.email,
            "created_at": str(emp.created_at) if emp.created_at else "",
            "updated_at": str(emp.updated_at) if emp.updated_at else "",
        })
    return {"employees": result}


@router.post("/employees")
async def register_employee(request: Dict[str, Any]):
    """注册员工"""
    manager = get_employee_manager()
    try:
        employee = manager.register(
            feishu_user_id=request["feishu_user_id"],
            name=request.get("name", ""),
            department=request.get("department", ""),
            skill_id=request.get("skill_id"),
            email=request.get("email", ""),
        )
        return {"success": True, "id": employee.id}
    except Exception as e:
        logger.error(f"Failed to register employee: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/employees/{feishu_user_id}/bind-skill")
async def bind_employee_skill(feishu_user_id: str, request: Dict[str, Any]):
    """绑定员工 Skill"""
    manager = get_employee_manager()
    skill_id = request.get("skill_id")
    if skill_id == "":
        skill_id = None
    success = manager.bind_skill(feishu_user_id, skill_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"success": True}


@router.get("/feishu/sessions")
async def list_feishu_sessions(limit: int = Query(50, le=200)):
    """获取飞书会话列表"""
    with get_db_session() as session:
        stmt = (
            select(FeishuSessionModel)
            .order_by(FeishuSessionModel.updated_at.desc())
            .limit(limit)
        )
        results = session.execute(stmt).scalars().all()
        sessions = []
        for s in results:
            sessions.append({
                "id": s.id,
                "feishu_user_id": s.feishu_user_id,
                "feishu_chat_id": s.feishu_chat_id,
                "employee_id": s.employee_id,
                "title": s.title,
                "message_count": s.message_count,
                "created_at": s.created_at,
                "updated_at": s.updated_at,
            })
        return {"sessions": sessions}


@router.get("/feishu/sessions/{session_id}/messages")
async def get_feishu_session_messages(
    session_id: str,
    limit: int = Query(50, le=100),
):
    """获取指定飞书会话的消息列表"""
    from database import MessageModel
    from sqlalchemy import select

    with get_db_session() as session:
        stmt = (
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.timestamp.asc())
            .limit(limit)
        )
        messages = session.execute(stmt).scalars().all()
        return {
            "messages": [
                {
                    "id": m.id,
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "metadata": m.metadata_json,
                }
                for m in messages
            ]
        }


# ==================== Obsidian 个人知识库 API ====================

@router.get("/employees/{employee_id}/vaults")
async def list_employee_vaults(employee_id: str):
    """获取员工的所有 Obsidian Vault"""
    try:
        from core.personal_knowledge import ObsidianVaultManager
        manager = ObsidianVaultManager()
        vaults = manager.get_by_employee(employee_id)
        return {
            "vaults": [
                {
                    "id": v.id,
                    "vault_name": v.vault_name,
                    "vault_path": v.vault_path,
                    "is_active": v.is_active,
                    "last_sync_at": v.last_sync_at,
                    "auto_sync": v.auto_sync,
                }
                for v in vaults
            ]
        }
    except Exception as e:
        logger.error(f"Failed to list vaults: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/employees/{employee_id}/vaults")
async def create_vault(employee_id: str, request: Dict[str, Any]):
    """创建 Obsidian Vault 配置"""
    try:
        from core.personal_knowledge import ObsidianVaultManager
        manager = ObsidianVaultManager()
        vault = manager.create_vault(
            employee_id=employee_id,
            vault_path=request["vault_path"],
            vault_name=request.get("vault_name", ""),
        )
        return {"success": True, "id": vault.id}
    except Exception as e:
        logger.error(f"Failed to create vault: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vaults/{vault_id}/sync")
async def sync_vault(vault_id: str):
    """手动同步 Vault"""
    try:
        from core.personal_knowledge import ObsidianVaultManager, ObsidianSyncer
        from database import get_db_session, ObsidianVaultModel
        from sqlalchemy import select

        with get_db_session() as session:
            stmt = select(ObsidianVaultModel).where(ObsidianVaultModel.id == vault_id)
            vault = session.execute(stmt).scalar_one_or_none()
            if not vault:
                raise HTTPException(status_code=404, detail="Vault not found")
            session.expunge(vault)

        syncer = ObsidianSyncer(vault)
        result = syncer.sync()

        vault_manager = ObsidianVaultManager()
        vault_manager.update_last_sync(vault_id)

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to sync vault: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/employees/{employee_id}/memories")
async def get_employee_memories(employee_id: str, memory_type: str = None):
    """获取员工个人记忆"""
    try:
        from core.personal_knowledge import PersonalMemoryManager
        manager = PersonalMemoryManager(employee_id)
        memories = manager.get_memories(memory_type=memory_type)
        return {"memories": memories}
    except Exception as e:
        logger.error(f"Failed to get memories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/employees/{employee_id}/memories")
async def add_memory(employee_id: str, request: Dict[str, Any]):
    """添加个人记忆"""
    try:
        from core.personal_knowledge import PersonalMemoryManager
        manager = PersonalMemoryManager(employee_id)
        memory = manager.add_memory(
            memory_type=request.get("memory_type", "preference"),
            memory_key=request["memory_key"],
            content=request["content"],
            summary=request.get("summary", ""),
            confidence=float(request.get("confidence", 0.8)),
        )
        return {"success": True, "id": memory.id}
    except Exception as e:
        logger.error(f"Failed to add memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/employees/{employee_id}/knowledge-graph")
async def get_knowledge_graph(employee_id: str, entity_name: str = None, depth: int = 2):
    """获取员工知识图谱"""
    try:
        from core.personal_knowledge import KnowledgeGraphManager

        if entity_name:
            manager = KnowledgeGraphManager(employee_id)
            entities = manager.get_related_entities(employee_id, entity_name, depth=depth)
            return {"entities": entities}
        else:
            from database import get_db_session, PersonalKnowledgeGraphModel
            from sqlalchemy import select

            with get_db_session() as session:
                stmt = select(PersonalKnowledgeGraphModel).where(
                    PersonalKnowledgeGraphModel.employee_id == employee_id
                ).order_by(
                    PersonalKnowledgeGraphModel.importance_score.desc()
                ).limit(100)

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
                    ]
                }
    except Exception as e:
        logger.error(f"Failed to get knowledge graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/employees/{employee_id}/notes")
async def get_employee_notes(
    employee_id: str,
    vault_id: str = None,
    limit: int = Query(50, le=200),
):
    """获取员工个人笔记"""
    try:
        from database import get_db_session, PersonalNoteModel
        from sqlalchemy import select

        with get_db_session() as session:
            stmt = select(PersonalNoteModel).where(
                PersonalNoteModel.employee_id == employee_id
            )
            if vault_id:
                stmt = stmt.where(PersonalNoteModel.vault_id == vault_id)
            stmt = stmt.order_by(PersonalNoteModel.last_modified.desc()).limit(limit)

            notes = session.execute(stmt).scalars().all()
            return {
                "notes": [
                    {
                        "id": n.id,
                        "title": n.title,
                        "file_name": n.file_name,
                        "tags": n.tags or [],
                        "word_count": n.word_count,
                        "last_modified": n.last_modified,
                        "is_processed": n.is_processed,
                    }
                    for n in notes
                ]
            }
    except Exception as e:
        logger.error(f"Failed to get notes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/employees/{employee_id}/personal-kb")
async def update_personal_kb_setting(employee_id: str, request: Dict[str, Any]):
    """更新员工个人知识库设置"""
    try:
        from feishu.employee_manager import EmployeeManager

        manager = EmployeeManager()
        metadata = request.get("metadata", {})

        employee = manager.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        current_metadata = employee.metadata_json or {}
        current_metadata.update(metadata)

        success = manager.update(employee_id, metadata_json=current_metadata)
        if not success:
            raise HTTPException(status_code=500, detail="Update failed")

        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update personal KB setting: {e}")
        raise HTTPException(status_code=500, detail=str(e))
