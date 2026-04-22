"""
员工个性化配置管理模块
负责员工注册、Skill 绑定、配置查询
"""

import uuid
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import (
    get_db_session,
    EmployeeModel,
    SkillTemplateModel,
    FeishuSessionModel,
    MessageModel,
)
from core.rag_engine import RAGResult

logger = logging.getLogger(__name__)


class EmployeeManager:
    """员工管理"""

    def __init__(self):
        pass

    def get_by_feishu_id(self, feishu_user_id: str) -> Optional[EmployeeModel]:
        with get_db_session() as session:
            stmt = select(EmployeeModel).where(
                EmployeeModel.feishu_user_id == feishu_user_id,
                EmployeeModel.is_active == True,
            )
            result = session.execute(stmt).scalar_one_or_none()
            if result:
                session.expunge(result)
            return result

    def get_by_id(self, employee_id: str) -> Optional[EmployeeModel]:
        with get_db_session() as session:
            stmt = select(EmployeeModel).where(EmployeeModel.id == employee_id)
            result = session.execute(stmt).scalar_one_or_none()
            if result:
                session.expunge(result)
            return result

    def register(
        self,
        feishu_user_id: str,
        name: str = "",
        department: str = "",
        skill_id: str = None,
        **kwargs,
    ) -> EmployeeModel:
        with get_db_session() as session:
            existing = session.execute(
                select(EmployeeModel).where(
                    EmployeeModel.feishu_user_id == feishu_user_id
                )
            ).scalar_one_or_none()

            if existing:
                existing.name = name
                existing.department = department
                if skill_id is not None:
                    existing.skill_id = skill_id
                existing.updated_at = datetime.now()
                for key, value in kwargs.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                employee = existing
            else:
                employee = EmployeeModel(
                    id=str(uuid.uuid4()),
                    feishu_user_id=feishu_user_id,
                    name=name,
                    department=department,
                    skill_id=skill_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    **{k: v for k, v in kwargs.items() if hasattr(EmployeeModel, k)},
                )
                session.add(employee)

            session.flush()
            session.expunge(employee)
            return employee

    def list_all(self, include_inactive: bool = False) -> List[EmployeeModel]:
        with get_db_session() as session:
            stmt = select(EmployeeModel)
            if not include_inactive:
                stmt = stmt.where(EmployeeModel.is_active == True)
            stmt = stmt.order_by(EmployeeModel.created_at.desc())
            results = session.execute(stmt).scalars().all()
            for r in results:
                session.expunge(r)
            return list(results)

    def bind_skill(self, feishu_user_id: str, skill_id: str) -> bool:
        employee = self.get_by_feishu_id(feishu_user_id)
        if not employee:
            return False
        with get_db_session() as session:
            stmt = select(EmployeeModel).where(
                EmployeeModel.feishu_user_id == feishu_user_id
            )
            emp = session.execute(stmt).scalar_one_or_none()
            if emp:
                emp.skill_id = skill_id
                emp.updated_at = datetime.now()
                return True
            return False

    def update(self, feishu_user_id: str, **fields) -> bool:
        with get_db_session() as session:
            stmt = select(EmployeeModel).where(
                EmployeeModel.feishu_user_id == feishu_user_id
            )
            emp = session.execute(stmt).scalar_one_or_none()
            if not emp:
                return False
            for key, value in fields.items():
                if hasattr(emp, key):
                    setattr(emp, key, value)
            emp.updated_at = datetime.now()
            return True

    def deactivate(self, feishu_user_id: str) -> bool:
        return self.update(feishu_user_id, is_active=False)

    def get_skill_for_user(self, feishu_user_id: str) -> Optional[SkillTemplateModel]:
        employee = self.get_by_feishu_id(feishu_user_id)
        if not employee or not employee.skill_id:
            return None
        skill_manager = SkillManager()
        return skill_manager.get_by_id(employee.skill_id)


class SkillManager:
    """Skill 模板管理"""

    DEFAULT_SKILLS = {
        "rigorous": {
            "id": "skill_rigorous",
            "name": "严谨型",
            "description": "适合严谨型员工，回答详细有逻辑，引用来源",
            "answer_style": "rigorous",
            "temperature": 0.3,
            "max_tokens": 3000,
            "system_prompt_suffix": (
                "你是一位严谨的知识库助手。回答要求：\n"
                "1. 回答必须基于提供的参考资料，不做任何推测\n"
                "2. 每个结论都要有明确的来源引用，格式为 [来源: 文档名]\n"
                "3. 回答结构采用分层级标题，使用编号列表\n"
                "4. 包含前提条件、适用范围、可能的风险点\n"
                "5. 如有不确定之处，明确标注并给出置信度\n"
                "6. 技术问题需给出完整的命令或代码示例"
            ),
            "knowledge_scope": ["技术文档", "规范文档", "操作手册"],
            "priority": 10,
        },
        "efficient": {
            "id": "skill_efficient",
            "name": "高效型",
            "description": "适合高智型员工，给出框架让对方自己推导",
            "answer_style": "efficient",
            "temperature": 0.5,
            "max_tokens": 1000,
            "system_prompt_suffix": (
                "你是一位高效的知识库助手。回答要求：\n"
                "1. 给出核心框架和关键节点，不做过度展开\n"
                "2. 使用结构化表达：问题→核心结论→关键支撑点\n"
                "3. 提供方向性指引和关键资源路径，让用户自行深入\n"
                "4. 用概念图或表格替代长段落\n"
                "5. 必要时用一句话总结核心答案"
            ),
            "knowledge_scope": ["战略文档", "架构设计", "技术方案"],
            "priority": 8,
        },
        "beginner": {
            "id": "skill_beginner",
            "name": "新人友好型",
            "description": "适合新人员工，回答通俗易懂，带日常比喻",
            "answer_style": "beginner",
            "temperature": 0.8,
            "max_tokens": 2000,
            "system_prompt_suffix": (
                "你是一位耐心的知识库助手，专为新人解答问题。回答要求：\n"
                "1. 使用通俗易懂的语言，避免专业术语或提供清晰解释\n"
                "2. 用日常生活中的比喻来解释抽象概念\n"
                "3. 给出具体可操作的步骤，每一步都有说明\n"
                "4. 在关键操作点提供截图指引或操作路径\n"
                "5. 预设常见误区和避坑提示\n"
                "6. 回答末尾给出延伸学习资源"
            ),
            "knowledge_scope": ["入门指南", "操作手册", "FAQ"],
            "priority": 9,
        },
        "default": {
            "id": "skill_default",
            "name": "默认风格",
            "description": "标准平衡风格，适合大多数场景",
            "answer_style": "balanced",
            "temperature": 0.7,
            "max_tokens": 2048,
            "system_prompt_suffix": (
                "你是一个专业的知识库问答助手。\n"
                "1. 基于提供的参考资料准确回答\n"
                "2. 如资料不足，坦诚告知用户\n"
                "3. 回答要引用来源，格式为 [来源: 文档名]\n"
                "4. 回答要结构清晰、重点突出"
            ),
            "knowledge_scope": [],
            "priority": 5,
        },
    }

    def __init__(self):
        try:
            self._ensure_default_skills()
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Failed to ensure default skills: {e}")

    def _ensure_default_skills(self):
        """确保默认 Skill 模板存在"""
        for skill_key, skill_data in self.DEFAULT_SKILLS.items():
            existing = self.get_by_id(skill_data["id"])
            if not existing:
                self._create_skill_from_dict(skill_data)

    def _create_skill_from_dict(self, data: Dict[str, Any]) -> SkillTemplateModel:
        with get_db_session() as session:
            now = datetime.now()
            skill = SkillTemplateModel(
                id=data["id"],
                name=data["name"],
                description=data["description"],
                system_prompt_suffix=data["system_prompt_suffix"],
                answer_style=data["answer_style"],
                temperature=data.get("temperature", 0.7),
                max_tokens=data.get("max_tokens", 2048),
                knowledge_scope=data.get("knowledge_scope", []),
                priority=data.get("priority", 0),
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            session.add(skill)
            session.flush()
            session.expunge(skill)
            return skill

    def get_by_id(self, skill_id: str) -> Optional[SkillTemplateModel]:
        with get_db_session() as session:
            stmt = select(SkillTemplateModel).where(
                SkillTemplateModel.id == skill_id,
                SkillTemplateModel.is_active == True,
            )
            result = session.execute(stmt).scalar_one_or_none()
            if result:
                session.expunge(result)
            return result

    def list_all(self, include_inactive: bool = False) -> List[SkillTemplateModel]:
        with get_db_session() as session:
            stmt = select(SkillTemplateModel)
            if not include_inactive:
                stmt = stmt.where(SkillTemplateModel.is_active == True)
            stmt = stmt.order_by(SkillTemplateModel.priority.desc())
            results = session.execute(stmt).scalars().all()
            for r in results:
                session.expunge(r)
            return list(results)

    def create(
        self,
        name: str,
        description: str = "",
        system_prompt_suffix: str = "",
        answer_style: str = "balanced",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        knowledge_scope: List[str] = None,
        priority: int = 0,
    ) -> SkillTemplateModel:
        skill_id = f"skill_{uuid.uuid4().hex[:8]}"
        now = datetime.now()
        with get_db_session() as session:
            skill = SkillTemplateModel(
                id=skill_id,
                name=name,
                description=description,
                system_prompt_suffix=system_prompt_suffix,
                answer_style=answer_style,
                temperature=temperature,
                max_tokens=max_tokens,
                knowledge_scope=knowledge_scope or [],
                priority=priority,
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            session.add(skill)
            session.flush()
            session.expunge(skill)
            return skill

    def update(self, skill_id: str, **fields) -> bool:
        with get_db_session() as session:
            stmt = select(SkillTemplateModel).where(
                SkillTemplateModel.id == skill_id
            )
            skill = session.execute(stmt).scalar_one_or_none()
            if not skill:
                return False
            for key, value in fields.items():
                if hasattr(skill, key):
                    setattr(skill, key, value)
            skill.updated_at = datetime.now()
            return True

    def delete(self, skill_id: str) -> bool:
        return self.update(skill_id, is_active=False)

    def get_default(self) -> Optional[SkillTemplateModel]:
        return self.get_by_id("skill_default")


class FeishuSessionManager:
    """飞书会话管理"""

    def __init__(self, max_history: int = 10):
        self.max_history = max_history

    def get_or_create(
        self,
        feishu_user_id: str,
        feishu_chat_id: str,
    ) -> FeishuSessionModel:
        with get_db_session() as session:
            stmt = select(FeishuSessionModel).where(
                FeishuSessionModel.feishu_user_id == feishu_user_id,
                FeishuSessionModel.feishu_chat_id == feishu_chat_id,
            )
            result = session.execute(stmt).scalar_one_or_none()
            if result:
                session.expunge(result)
                return result

            import time
            emp_manager = EmployeeManager()
            employee = emp_manager.get_by_feishu_id(feishu_user_id)

            session_id = str(uuid.uuid4())
            now = time.time()
            fs = FeishuSessionModel(
                id=session_id,
                feishu_user_id=feishu_user_id,
                feishu_chat_id=feishu_chat_id,
                employee_id=employee.id if employee else None,
                title=f"会话 {datetime.now().strftime('%m-%d %H:%M')}",
                created_at=now,
                updated_at=now,
            )
            session.add(fs)
            session.flush()
            session.expunge(fs)
            return fs

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Dict = None,
    ):
        import time
        with get_db_session() as session:
            msg_id = str(uuid.uuid4())
            msg = MessageModel(
                id=msg_id,
                session_id=session_id,
                role=role,
                content=content,
                timestamp=time.time(),
                metadata_json=metadata or {},
            )
            session.add(msg)

            stmt = select(FeishuSessionModel).where(
                FeishuSessionModel.id == session_id
            )
            fs = session.execute(stmt).scalar_one_or_none()
            if fs:
                fs.updated_at = time.time()
                fs.message_count += 1

    def get_history(
        self,
        session_id: str,
        limit: int = None,
    ) -> List[Dict]:
        limit = limit or self.max_history
        with get_db_session() as session:
            stmt = (
                select(MessageModel)
                .where(MessageModel.session_id == session_id)
                .order_by(MessageModel.timestamp.asc())
            )
            if limit:
                stmt = stmt.limit(limit)
            messages = session.execute(stmt).scalars().all()
            return [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp,
                }
                for m in messages
            ]


_employee_manager: Optional[EmployeeManager] = None
_skill_manager: Optional[SkillManager] = None
_feishu_session_manager: Optional[FeishuSessionManager] = None


def get_employee_manager() -> EmployeeManager:
    global _employee_manager
    if _employee_manager is None:
        _employee_manager = EmployeeManager()
    return _employee_manager


def get_skill_manager() -> SkillManager:
    global _skill_manager
    if _skill_manager is None:
        _skill_manager = SkillManager()
    return _skill_manager


def get_feishu_session_manager() -> FeishuSessionManager:
    global _feishu_session_manager
    if _feishu_session_manager is None:
        _feishu_session_manager = FeishuSessionManager()
    return _feishu_session_manager
