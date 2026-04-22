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
