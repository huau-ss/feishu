"""
存储模块
"""
from .document_storage import (
    DocumentStorage,
    DocumentRecord,
    get_document_storage,
)

__all__ = [
    "DocumentStorage",
    "DocumentRecord",
    "get_document_storage",
]
