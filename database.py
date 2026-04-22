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


class ObsidianVaultModel(Base):
    """Obsidian Vault 配置表"""
    __tablename__ = "obsidian_vaults"

    id = Column(String(36), primary_key=True)
    employee_id = Column(String(36), nullable=False, index=True)
    vault_path = Column(String(1024), nullable=False)
    vault_name = Column(String(256), default="")
    vault_url = Column(String(512), default="")
    access_token = Column(String(512), default="")
    is_active = Column(Boolean, default=True)
    last_sync_at = Column(Float, default=0)
    sync_interval_minutes = Column(Integer, default=30)
    auto_sync = Column(Boolean, default=True)
    include_folders = Column(JSON, default=[])
    exclude_folders = Column(JSON, default=["node_modules", ".git", ".obsidian"])
    file_extensions = Column(JSON, default=[".md"])
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class PersonalKnowledgeGraphModel(Base):
    """个人知识图谱实体表"""
    __tablename__ = "personal_knowledge_graph"

    id = Column(String(36), primary_key=True)
    employee_id = Column(String(36), nullable=False, index=True)
    entity_type = Column(String(64), default="concept")
    entity_name = Column(String(512), nullable=False)
    entity_aliases = Column(JSON, default=[])
    description = Column(Text, default="")
    source_note = Column(String(256), default="")
    importance_score = Column(Float, default=0.5)
    tags = Column(JSON, default=[])
    properties_json = Column(JSON, default={})
    embedding_vector_id = Column(String(128), default="")
    access_count = Column(Integer, default=0)
    last_accessed_at = Column(Float, default=0)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class KnowledgeRelationModel(Base):
    """知识关系表"""
    __tablename__ = "knowledge_relations"

    id = Column(String(36), primary_key=True)
    employee_id = Column(String(36), nullable=False, index=True)
    from_entity_id = Column(String(36), nullable=False, index=True)
    to_entity_id = Column(String(36), nullable=False, index=True)
    relation_type = Column(String(128), default="related_to")
    relation_label = Column(String(256), default="")
    weight = Column(Float, default=0.5)
    source_note = Column(String(256), default="")
    metadata_json = Column(JSON, default={})
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class PersonalNoteModel(Base):
    """个人笔记表"""
    __tablename__ = "personal_notes"

    id = Column(String(36), primary_key=True)
    employee_id = Column(String(36), nullable=False, index=True)
    vault_id = Column(String(36), nullable=True)
    file_path = Column(String(1024), nullable=False)
    file_name = Column(String(256), nullable=False)
    title = Column(String(512), default="")
    content = Column(Text, nullable=False)
    summary = Column(Text, default="")
    tags = Column(JSON, default=[])
    links = Column(JSON, default=[])
    back_links = Column(JSON, default=[])
    frontmatter_json = Column(JSON, default={})
    word_count = Column(Integer, default=0)
    hash_content = Column(String(64), default="")
    embedding_vector_id = Column(String(128), default="")
    last_modified = Column(Float, default=0)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class PersonalMemoryModel(Base):
    """员工个人记忆表 - 存储 AI 对员工的理解"""
    __tablename__ = "personal_memories"

    id = Column(String(36), primary_key=True)
    employee_id = Column(String(36), nullable=False, index=True)
    memory_type = Column(String(64), default="preference")
    memory_key = Column(String(256), nullable=False)
    memory_content = Column(Text, nullable=False)
    memory_summary = Column(String(512), default="")
    confidence = Column(Float, default=0.8)
    source_messages = Column(JSON, default=[])
    embedding_vector_id = Column(String(128), default="")
    access_count = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    expires_at = Column(Float, default=0)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


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
