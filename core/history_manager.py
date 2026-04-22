"""
对话历史与上下文管理模块
基于 MySQL 数据库的多会话管理、上下文记忆、自动摘要
"""
import uuid
import time
import logging
from typing import List, Dict, Optional, Any

from sqlalchemy import select, delete, or_

from database import get_db_session, init_database, SessionModel, MessageModel
from config.settings import settings

logger = logging.getLogger(__name__)


class Message:
    """聊天消息"""
    def __init__(
        self,
        id: str,
        role: str,
        content: str,
        timestamp: float = None,
        metadata: Dict[str, Any] = None,
    ):
        self.id = id
        self.role = role
        self.content = content
        self.timestamp = timestamp or time.time()
        self.metadata = metadata or {}


class Session:
    """会话"""
    def __init__(
        self,
        id: str,
        title: str,
        created_at: float,
        updated_at: float,
        messages: List[Message] = None,
        metadata: Dict[str, Any] = None,
    ):
        self.id = id
        self.title = title
        self.created_at = created_at
        self.updated_at = updated_at
        self.messages = messages or []
        self.metadata = metadata or {}


class HistoryManager:
    """
    对话历史管理器（MySQL 存储）

    功能：
    - 多会话管理
    - 上下文记忆（限制历史消息数量）
    - 会话持久化（MySQL 数据库）
    - 自动标题生成
    """

    def __init__(
        self,
        storage_path: str = None,
        max_history_messages: int = None,
        session_expire_hours: int = None,
    ):
        """
        Args:
            storage_path: 已废弃，保留参数兼容
            max_history_messages: 单个会话最大消息数
            session_expire_hours: 会话过期时间（小时）
        """
        self.max_history_messages = (
            max_history_messages or settings.MAX_HISTORY_MESSAGES
        )
        self.session_expire_hours = (
            session_expire_hours or settings.SESSION_EXPIRE_HOURS
        )
        self._initialized = False

    def _ensure_init(self):
        if not self._initialized:
            init_database()
            self._initialized = True

    def create_session(self, title: str = "", metadata: Dict = None) -> Session:
        """创建新会话"""
        self._ensure_init()
        session_id = str(uuid.uuid4())[:8]
        title = title or f"会话 {session_id}"
        now = time.time()

        with get_db_session() as session:
            model = SessionModel(
                id=session_id,
                title=title,
                created_at=now,
                updated_at=now,
                metadata_json=metadata or {},
            )
            session.add(model)

        logger.info(f"Created session: {session_id}")
        return Session(
            id=session_id,
            title=title,
            created_at=now,
            updated_at=now,
            messages=[],
            metadata=metadata or {},
        )

    def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话"""
        self._ensure_init()
        self._cleanup_expired()

        with get_db_session() as session:
            row = session.get(SessionModel, session_id)
            if not row:
                return None

            msg_rows = session.execute(
                select(MessageModel)
                .where(MessageModel.session_id == session_id)
                .order_by(MessageModel.timestamp)
            ).scalars().all()

            messages = [
                Message(
                    id=m.id,
                    role=m.role,
                    content=m.content,
                    timestamp=m.timestamp,
                    metadata=m.metadata_json or {},
                )
                for m in msg_rows
            ]

            return Session(
                id=row.id,
                title=row.title,
                created_at=row.created_at,
                updated_at=row.updated_at,
                messages=messages,
                metadata=row.metadata_json or {},
            )

    def delete_session(self, session_id: str) -> bool:
        """删除会话"""
        self._ensure_init()
        with get_db_session() as session:
            session.execute(
                delete(MessageModel).where(MessageModel.session_id == session_id)
            )
            row = session.get(SessionModel, session_id)
            if row:
                session.delete(row)
                return True
        return False

    def list_sessions(self, limit: int = 50) -> List[Session]:
        """列出所有会话（按更新时间排序）"""
        self._ensure_init()
        self._cleanup_expired()

        with get_db_session() as session:
            rows = session.execute(
                select(SessionModel)
                .order_by(SessionModel.updated_at.desc())
                .limit(limit)
            ).scalars().all()

            return [
                Session(
                    id=row.id,
                    title=row.title,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                    metadata=row.metadata_json or {},
                )
                for row in rows
            ]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Dict = None,
    ) -> Optional[Message]:
        """添加消息到会话"""
        self._ensure_init()

        now = time.time()
        message_id = str(uuid.uuid4())

        with get_db_session() as session:
            session_model = session.get(SessionModel, session_id)
            if not session_model:
                logger.warning(f"Session not found: {session_id}")
                return None

            msg_model = MessageModel(
                id=message_id,
                session_id=session_id,
                role=role,
                content=content,
                timestamp=now,
                metadata_json=metadata or {},
            )
            session.add(msg_model)

            session_model.updated_at = now

            count = session.query(MessageModel).filter(
                MessageModel.session_id == session_id
            ).count()
            if count > self.max_history_messages:
                oldest = session.execute(
                    select(MessageModel)
                    .where(MessageModel.session_id == session_id)
                    .order_by(MessageModel.timestamp)
                    .limit(count - self.max_history_messages)
                ).scalars().all()
                for m in oldest:
                    session.delete(m)

        return Message(
            id=message_id,
            role=role,
            content=content,
            timestamp=now,
            metadata=metadata or {},
        )

    def get_messages(
        self,
        session_id: str,
        limit: Optional[int] = None,
        include_system: bool = True,
    ) -> List[Message]:
        """获取会话消息"""
        self._ensure_init()

        with get_db_session() as session:
            stmt = select(MessageModel).where(
                MessageModel.session_id == session_id
            ).order_by(MessageModel.timestamp)

            rows = session.execute(stmt).scalars().all()

            messages = [
                Message(
                    id=row.id,
                    role=row.role,
                    content=row.content,
                    timestamp=row.timestamp,
                    metadata=row.metadata_json or {},
                )
                for row in rows
            ]

            if limit:
                messages = messages[-limit:]

            return messages

    def get_context(
        self,
        session_id: str,
        max_messages: int = 10,
    ) -> List[Dict[str, str]]:
        """
        获取对话上下文（用于 LLM）

        Returns:
            List[{"role": str, "content": str}]
        """
        messages = self.get_messages(session_id, limit=max_messages * 2)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    def clear_session(self, session_id: str) -> bool:
        """清空会话消息"""
        self._ensure_init()
        with get_db_session() as session:
            session.execute(
                delete(MessageModel).where(MessageModel.session_id == session_id)
            )
            row = session.get(SessionModel, session_id)
            if row:
                row.updated_at = time.time()
                return True
        return False

    def update_session_title(self, session_id: str, title: str) -> bool:
        """更新会话标题"""
        self._ensure_init()
        with get_db_session() as session:
            row = session.get(SessionModel, session_id)
            if row:
                row.title = title
                row.updated_at = time.time()
                return True
        return False

    def _cleanup_expired(self):
        """清理过期会话"""
        expire_time = self.session_expire_hours * 3600
        now = time.time()
        cutoff = now - expire_time

        with get_db_session() as session:
            expired_sessions = session.execute(
                select(SessionModel).where(SessionModel.updated_at < cutoff)
            ).scalars().all()

            expired_ids = [s.id for s in expired_sessions]

            if expired_ids:
                session.execute(
                    delete(MessageModel).where(
                        MessageModel.session_id.in_(expired_ids)
                    )
                )
                for s in expired_sessions:
                    session.delete(s)

                logger.info(f"Cleaned up {len(expired_ids)} expired sessions")

    def get_stats(self) -> Dict:
        """获取统计信息"""
        self._ensure_init()
        with get_db_session() as session:
            total_sessions = session.query(SessionModel).count()
            total_messages = session.query(MessageModel).count()
            return {
                "total_sessions": total_sessions,
                "total_messages": total_messages,
                "max_history_messages": self.max_history_messages,
                "session_expire_hours": self.session_expire_hours,
            }


# 全局实例
_default_manager: Optional[HistoryManager] = None


def get_history_manager() -> HistoryManager:
    """获取全局历史管理器"""
    global _default_manager
    if _default_manager is None:
        _default_manager = HistoryManager()
    return _default_manager
