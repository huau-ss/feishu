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

        matched_tags: List[str] = []

        query_keywords = extract_query_keywords(question, max_keywords=5)

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
        personalized_system = template_engine.build_system_prompt(
            base_system_prompt, skill_profile, query=question
        )

        context = ""
        if all_parents:
            context = self.rag_engine.build_context(all_parents)

        messages = [ChatMessage(role="system", content=personalized_system)]

        # 读取对话历史
        if session_id:
            history = self.session_manager.get_history(session_id)
            for hist in history[-10:]:  # 限制最近10条
                if hist["role"] == "user":
                    messages.append(ChatMessage(role="user", content=hist["content"]))
                elif hist["role"] == "assistant":
                    messages.append(ChatMessage(role="assistant", content=hist["content"]))

        if context:
            messages.append(
                ChatMessage(
                    role="user",
                    content=f"参考资料:\n{context}\n\n请根据以上参考资料回答问题。",
                )
            )
        messages.append(ChatMessage(role="user", content=question))

        active_llm = self.rag_engine.llm_client
        if not active_llm:
            active_llm = self.rag_engine.external_llm_client

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

        from_kb = bool(retrieved)
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
            answer_source="knowledge_base" if from_kb else "external_llm",
            sources=sources,
            query=question,
            retrieved_chunks=len(retrieved),
            reranked_chunks=len(reranked),
            used_chunks=len(all_parents),
            from_knowledge_base=from_kb,
            latency_ms=0.0,
            model=active_llm.model,
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
