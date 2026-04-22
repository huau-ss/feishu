"""
数据库连接与模型定义
使用 SQLAlchemy + PyMySQL 连接 MySQL 数据库
"""
import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Text,
    Float,
    DateTime,
    JSON,
    Boolean,
    BigInteger,
)
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy import text

from config.settings import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

DATABASE_URL = (
    f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}"
    f"@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"
    f"?charset={settings.MYSQL_CHARSET}"
)


class DocumentRecordModel(Base):
    """文档记录模型"""
    __tablename__ = "document_records"

    doc_id = Column(String(36), primary_key=True)
    title = Column(String(512), nullable=False)
    file_path = Column(String(1024), nullable=False)
    file_type = Column(String(32), nullable=False)
    file_size = Column(BigInteger, default=0)
    status = Column(String(32), default="pending")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    indexed_at = Column(DateTime, nullable=True)
    chunk_count = Column(Integer, default=0)
    error_msg = Column(Text, default="")
    metadata_json = Column(JSON, default={})


class MessageModel(Base):
    """聊天消息模型"""
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), nullable=False, index=True)
    role = Column(String(16), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(Float, nullable=False)
    metadata_json = Column(JSON, default={})


class SessionModel(Base):
    """会话模型"""
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True)
    title = Column(String(256), default="新会话")
    created_at = Column(Float, nullable=False)
    updated_at = Column(Float, nullable=False)
    metadata_json = Column(JSON, default={})


class CleanedDocumentModel(Base):
    """清洗后文档模型"""
    __tablename__ = "cleaned_documents"

    doc_id = Column(String(36), primary_key=True)
    title = Column(String(512), nullable=False)
    source_file = Column(String(1024), default="")
    file_type = Column(String(32), default="")
    doc_type = Column(String(32), default="")
    status = Column(String(16), default="cleaned")
    created_at = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, default={})
    warnings_json = Column(JSON, default=[])
    extra_metadata_json = Column(JSON, nullable=True)


class EmployeeModel(Base):
    """员工模型 - 飞书个性化 Bot 配置"""
    __tablename__ = "employees"

    id = Column(String(36), primary_key=True)
    feishu_user_id = Column(String(128), nullable=False, unique=True, index=True)
    name = Column(String(256), default="")
    department = Column(String(256), default="")
    role = Column(String(64), default="user")
    skill_id = Column(String(36), nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(512), default="")
    email = Column(String(256), default="")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    metadata_json = Column(JSON, default={})


class SkillTemplateModel(Base):
    """Skill 模板模型 - 定义回答风格配置"""
    __tablename__ = "skill_templates"

    id = Column(String(36), primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(512), default="")
    system_prompt_suffix = Column(Text, nullable=False)
    answer_style = Column(String(32), default="balanced")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=2048)
    knowledge_scope = Column(JSON, default=[])
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    metadata_json = Column(JSON, default={})


class FeishuSessionModel(Base):
    """飞书会话模型 - 追踪每个飞书用户的对话历史"""
    __tablename__ = "feishu_sessions"

    id = Column(String(36), primary_key=True)
    feishu_user_id = Column(String(128), nullable=False, index=True)
    feishu_chat_id = Column(String(128), nullable=False)
    employee_id = Column(String(36), nullable=True)
    title = Column(String(256), default="新会话")
    created_at = Column(Float, nullable=False)
    updated_at = Column(Float, nullable=False)
    message_count = Column(Integer, default=0)
    metadata_json = Column(JSON, default={})


_engine = None
_SessionLocal = None


def get_engine():
    """获取数据库引擎（延迟初始化）"""
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo=False,
        )
    return _engine


def get_session_factory():
    """获取 Session 工厂"""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )
    return _SessionLocal


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """获取数据库会话的上下文管理器"""
    SessionFactory = get_session_factory()
    session: Session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_database():
    """初始化数据库（创建所有表）"""
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized")
    except Exception as e:
        logger.warning(f"Database initialization skipped (MySQL may not be available): {e}")


def check_connection() -> bool:
    """检查数据库连接是否正常"""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
