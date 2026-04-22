"""
飞书 Bot 核心逻辑
消息接收 → 员工识别 → Skill 路由 → RAG 调用 → 消息回复
"""

import time
import logging
import hashlib
import hmac
import base64
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import json

from feishu.config import feishu_settings
from feishu.client import FeishuClient, FeishuAPIError, get_feishu_client
from feishu.employee_manager import (
    EmployeeManager,
    SkillManager,
    FeishuSessionManager,
    get_employee_manager,
    get_skill_manager,
    get_feishu_session_manager,
)
from llm import ChatMessage
from core.rag_engine import RAGEngine, RAGResult

logger = logging.getLogger(__name__)


@dataclass
class FeishuMessage:
    """飞书消息结构"""
    message_id: str
    sender_id: str
    sender_type: str
    chat_id: str
    content: str
    message_type: str
    create_time: str
    raw_event: Dict = field(default_factory=dict)


@dataclass
class BotResponse:
    """Bot 回复结构"""
    content: str
    sources: List[Dict] = field(default_factory=list)
    from_knowledge_base: bool = False
    skill_name: str = ""
    employee_name: str = ""
    answer_source: str = ""
    latency_ms: float = 0.0


class FeishuBot:
    """
    飞书 Bot 核心类

    处理流程:
    1. 接收飞书事件 (URL 验证 / 消息回调)
    2. 解析消息内容
    3. 查找/注册员工，获取其 Skill 配置
    4. 构建个性化 Prompt（Skill 风格）
    5. 调用 RAG Engine 获取回答
    6. 发送回复到飞书
    """

    def __init__(
        self,
        rag_engine: RAGEngine,
        feishu_client: FeishuClient = None,
        employee_manager: EmployeeManager = None,
        skill_manager: SkillManager = None,
        feishu_session_manager: FeishuSessionManager = None,
    ):
        self.rag_engine = rag_engine
        self.feishu_client = feishu_client or get_feishu_client()
        self.employee_manager = employee_manager or get_employee_manager()
        self.skill_manager = skill_manager or get_skill_manager()
        self.session_manager = feishu_session_manager or get_feishu_session_manager()

        self._rate_limit: Dict[str, List[float]] = {}

    def verify_webhook(self, challenge: str, verification_token: str) -> Dict:
        """
        验证飞书 Webhook URL

        飞书在设置企业自建应用时，会发送 GET 请求验证
        """
        if verification_token != feishu_settings.FEISHU_VERIFICATION_TOKEN:
            return {"code": 401, "msg": "verification token mismatch"}

        return {"code": 0, "challenge": challenge}

    def verify_signature(
        self,
        timestamp: str,
        nonce: str,
        body: str,
        signature: str,
    ) -> bool:
        """
        验证飞书事件签名（可选，用于安全性增强）
        """
        if not feishu_settings.FEISHU_APP_SECRET:
            return True

        s = f"{timestamp}{nonce}{body}"
        expected = hmac.new(
            feishu_settings.FEISHU_APP_SECRET.encode(),
            s.encode(),
            hashlib.sha256,
        ).digest()
        return hmac.compare_digest(
            base64.b64encode(expected).decode(),
            signature,
        )

    def parse_message(self, event: Dict) -> FeishuMessage:
        """解析飞书事件为统一的消息结构"""
        message_obj = event.get("message", {})
        sender = event.get("sender", {})
        content_str = message_obj.get("content", "{}")
        if isinstance(content_str, str):
            try:
                content = json.loads(content_str)
            except:
                content = {"text": content_str}
        else:
            content = content_str

        return FeishuMessage(
            message_id=message_obj.get("message_id", ""),
            sender_id=sender.get("sender_id", {}).get("open_id", ""),
            sender_type=sender.get("sender_type", "user"),
            chat_id=message_obj.get("chat_id", ""),
            content=content.get("text", ""),
            message_type=message_obj.get("message_type", "text"),
            create_time=message_obj.get("create_time", ""),
            raw_event=event,
        )

    def _check_rate_limit(self, user_id: str) -> bool:
        """检查用户请求频率限制"""
        now = time.time()
        if user_id not in self._rate_limit:
            self._rate_limit[user_id] = []

        self._rate_limit[user_id] = [
            t for t in self._rate_limit[user_id]
            if now - t < 60
        ]

        if len(self._rate_limit[user_id]) >= feishu_settings.FEISHU_RATE_LIMIT_PER_MINUTE:
            return False

        self._rate_limit[user_id].append(now)
        return True

    def _build_personalized_system_prompt(
        self,
        base_system_prompt: str,
        skill,
        employee,
        matched_tags: List[str],
    ) -> str:
        """根据员工 Skill 构建个性化系统提示词"""
        suffix = skill.system_prompt_suffix if skill else ""

        personal_lines = []
        if employee:
            if employee.name:
                personal_lines.append(f"当前用户姓名: {employee.name}")
            if employee.department:
                personal_lines.append(f"用户部门: {employee.department}")

        if matched_tags:
            personal_lines.append(f"当前问题涉及领域: {', '.join(matched_tags)}")

        personal_section = ""
        if personal_lines:
            personal_section = (
                "\n\n【用户信息】\n" +
                "\n".join(personal_lines) +
                "\n请根据上述用户信息和回答风格要求，调整你的回答方式。"
            )

        full_prompt = base_system_prompt
        if suffix:
            full_prompt = f"{full_prompt}\n\n{suffix}"
        if personal_section:
            full_prompt = f"{full_prompt}{personal_section}"

        return full_prompt

    def _get_knowledge_scope_filter(self, skill) -> Optional[Dict]:
        """根据 Skill 的知识范围构建检索过滤器"""
        if not skill or not skill.knowledge_scope:
            return None

        scope = skill.knowledge_scope
        if not scope:
            return None

        tags_filter = {"tags": {"$in": scope}}
        return tags_filter

    def _handle_kb_command(self, msg: FeishuMessage) -> Optional[BotResponse]:
        """处理知识库管理命令"""
        content = msg.content.strip()

        # 获取员工信息
        employee = self.employee_manager.get_by_feishu_id(msg.sender_id)
        if not employee:
            return None

        # 启用个人知识库
        if content.startswith("启用个人知识库") or content.startswith("开启赛博员工"):
            try:
                from feishu.employee_manager import EmployeeManager
                manager = EmployeeManager()
                current_meta = employee.metadata_json or {}
                current_meta["use_personal_kb"] = True
                manager.update(employee.id, metadata_json=current_meta)
                return BotResponse(
                    content="已为您启用个人知识库功能！\n\n"
                            "现在我可以：\n"
                            "• 记住您的偏好和工作背景\n"
                            "• 从您的对话中学习\n"
                            "• 提供更个性化的回答\n\n"
                            "发送「帮助」查看可用命令",
                    skill_name="",
                    employee_name=employee.name or "",
                )
            except Exception as e:
                logger.error(f"Failed to enable personal KB: {e}")
                return BotResponse(content=f"启用失败: {str(e)}", skill_name="", employee_name=employee.name or "")

        # 禁用个人知识库
        if content.startswith("禁用个人知识库") or content.startswith("关闭赛博员工"):
            try:
                from feishu.employee_manager import EmployeeManager
                manager = EmployeeManager()
                current_meta = employee.metadata_json or {}
                current_meta["use_personal_kb"] = False
                manager.update(employee.id, metadata_json=current_meta)
                return BotResponse(content="已关闭个人知识库功能。", skill_name="", employee_name=employee.name or "")
            except Exception as e:
                return BotResponse(content=f"操作失败: {str(e)}", skill_name="", employee_name=employee.name or "")

        # 检查是否启用了个人知识库
        use_personal_kb = employee.metadata_json.get("use_personal_kb", False)
        if not use_personal_kb:
            return None

        # 创建笔记命令
        if content.startswith("创建笔记") or content.startswith("新建笔记"):
            return self._cmd_create_note(msg, employee)

        # 查看笔记列表
        if content.startswith("查看笔记") or content.startswith("我的笔记") or content == "笔记列表":
            return self._cmd_list_notes(msg, employee)

        # 搜索笔记
        if content.startswith("搜索笔记") or content.startswith("查找笔记"):
            return self._cmd_search_notes(msg, employee)

        # 删除笔记
        if content.startswith("删除笔记"):
            return self._cmd_delete_note(msg, employee)

        # 查看知识图谱
        if content == "我的知识图谱" or content == "知识图谱":
            return self._cmd_show_graph(msg, employee)

        # 查看记忆
        if content == "我的记忆" or content == "查看记忆":
            return self._cmd_show_memories(msg, employee)

        # 帮助命令
        if content == "帮助" or content == "help":
            return self._cmd_help(employee)

        return None

    def _cmd_create_note(self, msg: FeishuMessage, employee) -> BotResponse:
        """创建笔记"""
        content = msg.content.strip()
        title = ""
        note_content = ""
        tags = []

        lines = content.split("\n")
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("标题:"):
                title = line[3:].strip()
            elif line.startswith("内容:"):
                note_content = line[3:].strip()
            elif line.startswith("标签:"):
                tags = [t.strip() for t in line[3:].split(",")]

        if not title:
            return BotResponse(
                content="请告诉我笔记的标题和内容：\n\n格式：\n创建笔记\n标题: 我的笔记标题\n内容: 笔记内容...",
                skill_name="", employee_name=employee.name or "",
            )

        if not note_content:
            return BotResponse(
                content=f"笔记标题: **{title}**\n\n请告诉我笔记内容：",
                skill_name="", employee_name=employee.name or "",
            )

        try:
            from core.personal_knowledge import PersonalNoteManager
            manager = PersonalNoteManager()
            manager.upsert_note(
                employee_id=employee.id,
                file_path=f"personal/{employee.id}/{title}.md",
                file_name=f"{title}.md",
                title=title, content=note_content, tags=tags,
            )
            return BotResponse(
                content=f"笔记已保存！\n\n**{title}**\n{note_content[:200]}{'...' if len(note_content) > 200 else ''}",
                skill_name="", employee_name=employee.name or "",
            )
        except Exception as e:
            logger.error(f"Failed to create note: {e}")
            return BotResponse(content=f"保存笔记失败: {str(e)}", skill_name="", employee_name=employee.name or "")

    def _cmd_list_notes(self, msg: FeishuMessage, employee) -> BotResponse:
        """列出笔记"""
        try:
            from database import get_db_session, PersonalNoteModel
            from sqlalchemy import select

            with get_db_session() as session:
                stmt = select(PersonalNoteModel).where(
                    PersonalNoteModel.employee_id == employee.id
                ).order_by(PersonalNoteModel.updated_at.desc()).limit(20)
                notes = session.execute(stmt).scalars().all()

            if not notes:
                return BotResponse(content="您还没有创建任何笔记。发送「创建笔记」开始记录！", skill_name="", employee_name=employee.name or "")

            lines = [f"**您的笔记** (共 {len(notes)} 篇)\n"]
            for i, note in enumerate(notes, 1):
                tags_str = f" [{', '.join(note.tags)}]" if note.tags else ""
                lines.append(f"{i}. **{note.title}**{tags_str}")

            lines.append("\n回复「查看笔记 + 序号」查看详情")
            return BotResponse(content="\n".join(lines), skill_name="", employee_name=employee.name or "")
        except Exception as e:
            logger.error(f"Failed to list notes: {e}")
            return BotResponse(content=f"获取笔记列表失败: {str(e)}", skill_name="", employee_name=employee.name or "")

    def _cmd_search_notes(self, msg: FeishuMessage, employee) -> BotResponse:
        """搜索笔记"""
        content = msg.content.strip()
        keyword = content.replace("搜索笔记", "").replace("查找笔记", "").strip()

        if not keyword:
            return BotResponse(content="请告诉我搜索关键词：\n格式：搜索笔记 + 关键词", skill_name="", employee_name=employee.name or "")

        try:
            from database import get_db_session, PersonalNoteModel
            from sqlalchemy import select

            with get_db_session() as session:
                stmt = select(PersonalNoteModel).where(
                    PersonalNoteModel.employee_id == employee.id
                ).order_by(PersonalNoteModel.updated_at.desc())
                all_notes = session.execute(stmt).scalars().all()

            results = [n for n in all_notes if keyword.lower() in n.title.lower() or keyword.lower() in n.content.lower()]

            if not results:
                return BotResponse(content=f"没有找到包含「{keyword}」的笔记", skill_name="", employee_name=employee.name or "")

            lines = [f"找到 {len(results)} 篇相关笔记:\n"]
            for i, note in enumerate(results[:5], 1):
                preview = note.content[:50] + "..." if len(note.content) > 50 else note.content
                lines.append(f"{i}. **{note.title}**\n   {preview}")

            return BotResponse(content="\n".join(lines), skill_name="", employee_name=employee.name or "")
        except Exception as e:
            return BotResponse(content=f"搜索失败: {str(e)}", skill_name="", employee_name=employee.name or "")

    def _cmd_delete_note(self, msg: FeishuMessage, employee) -> BotResponse:
        """删除笔记"""
        content = msg.content.strip()
        note_title = content.replace("删除笔记", "").strip()

        if not note_title:
            return BotResponse(content="请告诉我删除哪篇笔记：\n格式：删除笔记 + 标题", skill_name="", employee_name=employee.name or "")

        try:
            from database import get_db_session, PersonalNoteModel
            from sqlalchemy import select, and_

            with get_db_session() as session:
                stmt = select(PersonalNoteModel).where(
                    and_(PersonalNoteModel.employee_id == employee.id, PersonalNoteModel.title == note_title)
                )
                note = session.execute(stmt).scalar_one_or_none()
                if not note:
                    return BotResponse(content=f"没有找到笔记「{note_title}」", skill_name="", employee_name=employee.name or "")
                session.delete(note)

            return BotResponse(content=f"已删除笔记「{note_title}」", skill_name="", employee_name=employee.name or "")
        except Exception as e:
            return BotResponse(content=f"删除失败: {str(e)}", skill_name="", employee_name=employee.name or "")

    def _cmd_show_graph(self, msg: FeishuMessage, employee) -> BotResponse:
        """显示知识图谱"""
        try:
            from database import get_db_session, PersonalKnowledgeGraphModel
            from sqlalchemy import select

            with get_db_session() as session:
                stmt = select(PersonalKnowledgeGraphModel).where(
                    PersonalKnowledgeGraphModel.employee_id == employee.id
                ).order_by(PersonalKnowledgeGraphModel.importance_score.desc()).limit(15)
                entities = session.execute(stmt).scalars().all()

            if not entities:
                return BotResponse(content="您的知识图谱还是空的。随着对话和笔记的积累，我会帮您构建个人知识图谱。", skill_name="", employee_name=employee.name or "")

            lines = ["**您的知识图谱**\n"]
            by_type = {}
            for e in entities:
                t = e.entity_type or "概念"
                if t not in by_type:
                    by_type[t] = []
                by_type[t].append(e.entity_name)

            for t, names in by_type.items():
                lines.append(f"\n**{t}**: {', '.join(names[:8])}")

            lines.append(f"\n\n共 {len(entities)} 个概念")
            return BotResponse(content="\n".join(lines), skill_name="", employee_name=employee.name or "")
        except Exception as e:
            return BotResponse(content=f"获取知识图谱失败: {str(e)}", skill_name="", employee_name=employee.name or "")

    def _cmd_show_memories(self, msg: FeishuMessage, employee) -> BotResponse:
        """显示个人记忆"""
        try:
            from database import get_db_session, PersonalMemoryModel
            from sqlalchemy import select

            with get_db_session() as session:
                stmt = select(PersonalMemoryModel).where(
                    PersonalMemoryModel.employee_id == employee.id
                ).order_by(PersonalMemoryModel.confidence.desc()).limit(10)
                memories = session.execute(stmt).scalars().all()

            if not memories:
                return BotResponse(content="您还没有个人记忆。我会从对话中自动学习关于您的信息。", skill_name="", employee_name=employee.name or "")

            lines = ["**关于您的记忆**\n"]
            by_type = {}
            for m in memories:
                t = m.memory_type or "其他"
                if t not in by_type:
                    by_type[t] = []
                by_type[t].append(m.memory_summary or m.memory_content[:50])

            for t, items in by_type.items():
                lines.append(f"\n**{t}**:")
                for item in items[:3]:
                    lines.append(f"• {item}...")

            return BotResponse(content="\n".join(lines), skill_name="", employee_name=employee.name or "")
        except Exception as e:
            return BotResponse(content=f"获取记忆失败: {str(e)}", skill_name="", employee_name=employee.name or "")

    def _cmd_help(self, employee) -> BotResponse:
        """显示帮助"""
        return BotResponse(
            content="**赛博员工助手 - 命令列表**\n\n"
                    "**笔记管理**\n"
                    "• 创建笔记 - 新建笔记\n"
                    "• 查看笔记 - 查看笔记列表\n"
                    "• 搜索笔记 + 关键词 - 搜索笔记\n"
                    "• 删除笔记 + 标题 - 删除笔记\n\n"
                    "**知识库**\n"
                    "• 我的知识图谱 - 查看知识图谱\n"
                    "• 我的记忆 - 查看个人记忆\n\n"
                    "**设置**\n"
                    "• 启用个人知识库 - 开启赛博员工\n"
                    "• 禁用个人知识库 - 关闭赛博员工\n\n"
                    "直接问我任何问题，我会结合您的个人知识库回答",
            skill_name="", employee_name=employee.name or "",
        )

    def handle_message(self, event: Dict) -> Optional[BotResponse]:
        """
        处理飞书消息事件

        Args:
            event: 飞书事件 payload

        Returns:
            BotResponse: 处理结果（用于发送回复）
        """
        try:
            msg = self.parse_message(event)
        except Exception as e:
            logger.error(f"Failed to parse message: {e}")
            return None

        if not msg.content or not msg.sender_id:
            return None

        if not self._check_rate_limit(msg.sender_id):
            logger.warning(f"Rate limit exceeded for user {msg.sender_id}")
            return BotResponse(
                content="请求过于频繁，请稍后再试。",
                skill_name="",
                employee_name="",
            )

        logger.info(
            f"Processing message from user={msg.sender_id}, "
            f"chat={msg.chat_id}, content_len={len(msg.content)}"
        )

        return self._do_query(msg)

    def _do_query(self, msg: FeishuMessage) -> BotResponse:
        """执行业务查询"""
        # 检查是否是对话管理命令
        command_result = self._handle_kb_command(msg)
        if command_result:
            return command_result

        start_time = time.time()

        employee = self.employee_manager.get_by_feishu_id(msg.sender_id)
        if not employee:
            try:
                employee = self.employee_manager.register(
                    feishu_user_id=msg.sender_id,
                    name=msg.raw_event.get("sender", {}).get("sender_id", {}).get("open_id", ""),
                )
                logger.info(f"Auto-registered new user: {msg.sender_id}")
            except Exception as e:
                logger.warning(f"Failed to auto-register user: {e}")
                employee = None

        skill = None
        if employee and employee.skill_id:
            skill = self.skill_manager.get_by_id(employee.skill_id)
        if not skill:
            skill = self.skill_manager.get_default()

        skill_name = skill.name if skill else "默认"
        employee_name = employee.name if employee else ""

        temperature = skill.temperature if skill else 0.7
        max_tokens = skill.max_tokens if skill else 2048

        session = self.session_manager.get_or_create(
            feishu_user_id=msg.sender_id,
            feishu_chat_id=msg.chat_id,
        )

        matched_tags: List[str] = []
        try:
            result = self._query_with_skill(
                question=msg.content,
                skill=skill,
                employee=employee,
                session_id=session.id,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            matched_tags = result.metadata.get("matched_tags", [])
            answer = result.answer
            from_kb = result.from_knowledge_base
            answer_source = result.answer_source
            sources = result.sources
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            answer = f"抱歉，处理您的请求时遇到问题：{str(e)}"
            from_kb = False
            answer_source = "error"
            sources = []

        try:
            self.session_manager.add_message(
                session_id=session.id,
                role="user",
                content=msg.content,
                metadata={"feishu_message_id": msg.message_id},
            )
            self.session_manager.add_message(
                session_id=session.id,
                role="assistant",
                content=answer,
                metadata={"skill_id": skill.id if skill else None, "from_kb": from_kb},
            )
        except Exception as e:
            logger.warning(f"Failed to save to session history: {e}")

        # 赛博员工：从对话中学习
        if employee and employee.metadata_json.get("use_personal_kb", False):
            try:
                from core.personal_rag import CyberEmployeeBuilder
                cyber_builder = CyberEmployeeBuilder(employee.id)
                cyber_builder.learn_from_conversation(msg.content, answer)
            except Exception as e:
                logger.warning(f"Failed to learn from conversation: {e}")

        latency = (time.time() - start_time) * 1000

        return BotResponse(
            content=answer,
            sources=sources,
            from_knowledge_base=from_kb,
            skill_name=skill_name,
            employee_name=employee_name,
            answer_source=answer_source,
            latency_ms=latency,
        )

    def _query_with_skill(
        self,
        question: str,
        skill,
        employee,
        session_id: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> RAGResult:
        """使用 Skill 个性化配置执行 RAG 查询"""
        from core.rag_engine import RAGResult
        from core.chunker import extract_query_keywords
        from core.skill_templates import SkillProfile, get_skill_template_engine
        from core.personal_rag import CyberEmployeeBuilder, PersonalRAGConfig

        matched_tags: List[str] = []
        employee_id = employee.id if employee else None

        # 检查是否启用了个人知识库
        use_personal_kb = employee and employee.metadata_json.get("use_personal_kb", False)

        query_keywords = extract_query_keywords(question, max_keywords=5)

        # 1. 检索共享知识库
        retrieved = self.rag_engine.retrieve(question)
        reranked = []
        all_parents = []

        if retrieved:
            reranked = self.rag_engine.rerank_chunks_with_tags(
                question, retrieved, query_keywords
            )
            if reranked:
                all_parents = self.rag_engine.get_parent_chunks(reranked)

                from collections import Counter
                all_tags = []
                for chunk in all_parents:
                    all_tags.extend(chunk.metadata.get("tags", []))
                tag_counts = Counter(all_tags)
                matched_tags = [t for t, _ in tag_counts.most_common(3)]

        skill_profile = SkillProfile(
            skill_id=skill.id if skill else "default",
            name=skill.name if skill else "默认",
            answer_style=skill.answer_style if skill else "balanced",
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt_suffix=skill.system_prompt_suffix if skill else "",
            knowledge_scope=skill.knowledge_scope if skill else [],
            matched_tags=matched_tags,
        )

        template_engine = get_skill_template_engine()
        base_system_prompt = self.rag_engine.SYSTEM_PROMPT

        # 构建上下文（共享KB + 个人知识库 + 知识图谱）
        kb_context = ""
        if all_parents:
            kb_context = self.rag_engine.build_context(all_parents)

        personal_context = ""
        personal_has_content = False
        if use_personal_kb and employee_id:
            try:
                cyber_builder = CyberEmployeeBuilder(employee_id)
                personal_results = cyber_builder.personal_rag.query(question)
                personal_context = personal_results.get("final_context", "")
                personal_has_content = bool(personal_results.get("personal_chunks") or
                                            personal_results.get("graph_entities") or
                                            personal_results.get("memories"))

                logger.info(
                    f"Personal KB: {len(personal_results.get('personal_chunks', []))} chunks, "
                    f"Graph: {len(personal_results.get('graph_entities', []))} entities, "
                    f"has_content={personal_has_content}"
                )
            except Exception as e:
                logger.warning(f"Personal KB query failed: {e}")

        # 构建系统提示词
        personalized_system = template_engine.build_system_prompt(
            base_system_prompt, skill_profile, query=question
        )

        # 如果有赛博员工配置，加入个性化上下文
        if use_personal_kb and employee_id:
            try:
                cyber_builder = CyberEmployeeBuilder(employee_id)
                profile_prompt = cyber_builder.build_profile_prompt()
                if profile_prompt:
                    personalized_system += "\n\n" + profile_prompt
            except Exception as e:
                logger.warning(f"Failed to build profile prompt: {e}")

        messages = [ChatMessage(role="system", content=personalized_system)]

        # 读取对话历史
        if session_id:
            history = self.session_manager.get_history(session_id)
            for hist in history[-10:]:
                if hist["role"] == "user":
                    messages.append(ChatMessage(role="user", content=hist["content"]))
                elif hist["role"] == "assistant":
                    messages.append(ChatMessage(role="assistant", content=hist["content"]))

        # 决策：知识库（共享KB 或 个人KB）有内容 → 本地 LLM；都没有 → 公网 LLM
        shared_has_content = bool(all_parents)
        from_kb = shared_has_content or personal_has_content

        if from_kb:
            # 知识库有结果：添加上下文，使用本地 LLM
            context_parts = []
            if kb_context:
                context_parts.append(f"## 共享知识库\n{kb_context}")
            if personal_context:
                context_parts.append(f"## 个人知识\n{personal_context}")

            messages.append(
                ChatMessage(
                    role="user",
                    content="【参考资料】\n" + "\n\n".join(context_parts) + "\n\n请根据以上参考资料，结合上下文对话历史回答问题。",
                )
            )
            messages.append(ChatMessage(role="user", content=question))

            active_llm = self.rag_engine.llm_client
            if not active_llm:
                return RAGResult(
                    answer="LLM 未配置，请联系管理员。",
                    answer_source="error",
                    query=question,
                )

            response = active_llm.chat(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            answer_source = "knowledge_base"
        else:
            # 知识库没有结果：公网大模型兜底
            messages.append(ChatMessage(role="user", content=question))

            external_llm = self.rag_engine.external_llm_client
            if not external_llm:
                return RAGResult(
                    answer="本地知识库和个人笔记中未找到相关内容，同时未配置公网大模型，无法回答您的问题。",
                    answer_source="none",
                    query=question,
                )

            response = external_llm.chat(
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            answer_source = "external_llm"
            logger.info("KB empty, falling back to external LLM")

        sources = [
            {
                "title": chunk.metadata.get("title", "未知"),
                "content": chunk.content[:200],
                "score": chunk.score,
                "tags": chunk.metadata.get("tags", []),
            }
            for chunk in all_parents
        ]

        return RAGResult(
            answer=response.content,
            answer_source=answer_source,
            sources=sources,
            query=question,
            retrieved_chunks=len(retrieved),
            reranked_chunks=len(reranked),
            used_chunks=len(all_parents),
            from_knowledge_base=from_kb,
            latency_ms=0.0,
            model=response.model,
            metadata={"matched_tags": matched_tags},
        )

    def send_reply(self, msg: FeishuMessage, response: BotResponse) -> bool:
        """发送回复到飞书"""
        try:
            source_label = "知识库" if response.from_knowledge_base else "AI 生成"
            if response.answer_source == "error":
                source_label = "处理异常"

            header = f"💬 {response.skill_name}"
            if response.employee_name:
                header = f"💬 {response.employee_name} · {response.skill_name}"

            card = self.feishu_client.build_text_card(
                header_text=header,
                answer=response.content,
                sources=response.sources,
                employee_name=response.employee_name,
                skill_name=response.skill_name,
                source_label=source_label,
            )

            self.feishu_client.send_interactive_card(
                receive_id=msg.chat_id,
                card_content=card,
            )
            logger.info(
                f"Sent reply to chat={msg.chat_id}, "
                f"source={response.answer_source}, latency={response.latency_ms:.0f}ms"
            )
            return True

        except FeishuAPIError as e:
            logger.error(f"Failed to send reply: {e}")
            fallback_text = f"{response.content}\n\n_发送失败: {e.msg}_"
            try:
                self.feishu_client.send_text_message(msg.chat_id, fallback_text[:2000])
            except Exception:
                pass
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending reply: {e}")
            return False


_default_bot: Optional[FeishuBot] = None


def get_feishu_bot(rag_engine: RAGEngine = None) -> FeishuBot:
    global _default_bot
    if _default_bot is None:
        from core import get_rag_engine
        _default_bot = FeishuBot(
            rag_engine=rag_engine or get_rag_engine(),
        )
    return _default_bot
