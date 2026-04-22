"""
文档存储模块
基于 MySQL 数据库的文档管理
"""
import uuid
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session

from database import (
    get_db_session,
    init_database,
    DocumentRecordModel,
)
from config.settings import settings

logger = logging.getLogger(__name__)


class DocumentStorage:
    """
    MySQL 文档存储

    功能：
    - 文档元数据管理
    - 状态跟踪
    - 去重检查
    """

    def __init__(self, storage_dir: str = None):
        self._initialized = False

    def _ensure_init(self):
        if not self._initialized:
            init_database()
            self._initialized = True

    def add(
        self,
        title: str,
        file_path: str,
        file_type: str,
        file_size: int,
        metadata: Dict = None,
    ) -> "DocumentRecord":
        """添加文档记录"""
        self._ensure_init()
        doc_id = str(uuid.uuid4())
        now = datetime.now()

        record = DocumentRecord(
            doc_id=doc_id,
            title=title,
            file_path=str(file_path),
            file_type=file_type,
            file_size=file_size,
            status="pending",
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
        )

        with get_db_session() as session:
            model = DocumentRecordModel(
                doc_id=doc_id,
                title=title,
                file_path=str(file_path),
                file_type=file_type,
                file_size=file_size,
                status="pending",
                created_at=now,
                updated_at=now,
                metadata_json=metadata or {},
            )
            session.add(model)

        logger.info(f"Added document: {doc_id} - {title}")
        return record

    def get(self, doc_id: str) -> Optional["DocumentRecord"]:
        """获取文档记录"""
        self._ensure_init()
        with get_db_session() as session:
            row = session.get(DocumentRecordModel, doc_id)
            if row:
                return self._row_to_record(row)
        return None

    def update_status(
        self,
        doc_id: str,
        status: str,
        error_msg: str = "",
        chunk_count: int = 0,
    ) -> bool:
        """更新文档状态"""
        self._ensure_init()
        with get_db_session() as session:
            row = session.get(DocumentRecordModel, doc_id)
            if row:
                row.status = status
                row.updated_at = datetime.now()
                row.error_msg = error_msg
                if chunk_count > 0:
                    row.chunk_count = chunk_count
                if status == "indexed":
                    row.indexed_at = datetime.now()
                return True
        return False

    def delete(self, doc_id: str) -> bool:
        """删除文档记录"""
        self._ensure_init()
        with get_db_session() as session:
            row = session.get(DocumentRecordModel, doc_id)
            if row:
                session.delete(row)
                return True
        return False

    def list_all(self, status: str = None) -> List["DocumentRecord"]:
        """列出所有文档"""
        self._ensure_init()
        with get_db_session() as session:
            stmt = select(DocumentRecordModel)
            if status:
                stmt = stmt.where(DocumentRecordModel.status == status)
            stmt = stmt.order_by(DocumentRecordModel.updated_at.desc())
            rows = session.execute(stmt).scalars().all()
            return [self._row_to_record(row) for row in rows]

    def get_stats(self) -> Dict:
        """获取统计信息"""
        self._ensure_init()
        with get_db_session() as session:
            total = session.query(func.count(DocumentRecordModel.doc_id)).scalar()

            status_counts = {}
            rows = session.execute(
                select(
                    DocumentRecordModel.status,
                    func.count(DocumentRecordModel.doc_id),
                ).group_by(DocumentRecordModel.status)
            ).all()
            for row in rows:
                status_counts[row[0]] = row[1]

            total_size = session.query(
                func.sum(DocumentRecordModel.file_size)
            ).scalar() or 0

            total_chunks = session.query(
                func.sum(DocumentRecordModel.chunk_count)
            ).scalar() or 0

            return {
                "total_documents": total,
                "status_counts": status_counts,
                "total_size_bytes": total_size,
                "total_chunks": total_chunks,
            }

    def clear_all(self):
        """清空所有记录"""
        self._ensure_init()
        with get_db_session() as session:
            session.execute(delete(DocumentRecordModel))

    def _row_to_record(self, row: DocumentRecordModel) -> "DocumentRecord":
        """将数据库行转换为 DocumentRecord"""
        return DocumentRecord(
            doc_id=row.doc_id,
            title=row.title,
            file_path=row.file_path,
            file_type=row.file_type,
            file_size=row.file_size,
            status=row.status,
            created_at=row.created_at.isoformat() if row.created_at else "",
            updated_at=row.updated_at.isoformat() if row.updated_at else "",
            indexed_at=row.indexed_at.isoformat() if row.indexed_at else None,
            chunk_count=row.chunk_count,
            error_msg=row.error_msg,
            metadata=row.metadata_json or {},
        )


class DocumentRecord:
    """文档记录（与原 JSON 版本接口兼容）"""
    def __init__(
        self,
        doc_id: str,
        title: str,
        file_path: str,
        file_type: str,
        file_size: int,
        status: str,
        created_at: str,
        updated_at: str,
        indexed_at: Optional[str] = None,
        chunk_count: int = 0,
        error_msg: str = "",
        metadata: Dict[str, Any] = None,
    ):
        self.doc_id = doc_id
        self.title = title
        self.file_path = file_path
        self.file_type = file_type
        self.file_size = file_size
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.indexed_at = indexed_at
        self.chunk_count = chunk_count
        self.error_msg = error_msg
        self.metadata = metadata or {}


# 全局实例
_default_storage: Optional[DocumentStorage] = None


def get_document_storage() -> DocumentStorage:
    """获取全局文档存储"""
    global _default_storage
    if _default_storage is None:
        _default_storage = DocumentStorage()
    return _default_storage
