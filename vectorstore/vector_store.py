"""
向量数据库模块
支持 Qdrant 和 ChromaDB
"""
import json
import logging
import uuid
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """文档对象"""
    id: str
    content: str
    vector: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
        }


@dataclass
class SearchResult:
    """搜索结果"""
    id: str
    content: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_id: Optional[str] = None
    is_parent: bool = False


class VectorStore:
    """向量数据库基类"""

    def add(self, documents: List[Document]) -> bool:
        """添加文档"""
        raise NotImplementedError

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[SearchResult]:
        """向量检索"""
        raise NotImplementedError

    def search_by_text(
        self,
        query_text: str,
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[SearchResult]:
        """文本检索（需外部编码）"""
        raise NotImplementedError

    def delete(self, doc_ids: List[str]) -> bool:
        """删除文档"""
        raise NotImplementedError

    def count(self) -> int:
        """统计文档数量"""
        raise NotImplementedError

    def clear(self) -> bool:
        """清空集合"""
        raise NotImplementedError


class QdrantStore(VectorStore):
    """
    Qdrant 向量数据库

    需要 Qdrant 服务运行在 localhost:6333
    """

    def __init__(
        self,
        collection_name: str = "knowledge_base",
        vector_dim: int = 1024,
        host: str = "localhost",
        port: int = 6333,
        grpc_port: int = 6334,
        distance: str = "Cosine",
    ):
        self.collection_name = collection_name
        self.vector_dim = vector_dim
        self.host = host
        self.port = port
        self.grpc_port = grpc_port
        self.distance = distance
        self._client = None
        self._collection_ready = False

    @property
    def client(self):
        """懒加载客户端"""
        if self._client is None:
            try:
                from qdrant_client import QdrantClient
                from qdrant_client.http import models
            except ImportError:
                raise ImportError("请安装 qdrant-client: pip install qdrant-client")

            self._client = QdrantClient(
                host=self.host,
                port=self.port,
                grpc_port=self.grpc_port,
            )
        return self._client

    def ensure_collection(self) -> bool:
        """确保 Collection 存在"""
        if self._collection_ready:
            return True

        try:
            from qdrant_client.http import models
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                # 移除 optimizers_config，新版本不需要或使用默认值
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_dim,
                        distance=models.Distance.COSINE,
                    ),
                )
                logger.info(f"Created collection: {self.collection_name}")

            self._collection_ready = True
            return True

        except Exception as e:
            logger.error(f"Failed to ensure collection: {e}")
            return False

    def add(self, documents: List[Document]) -> bool:
        """添加文档到 Qdrant"""
        if not documents:
            return True

        self.ensure_collection()

        from qdrant_client.http import models

        import uuid

        points = []
        for doc in documents:
            if doc.vector is None:
                logger.warning(f"Document {doc.id} has no vector, skipping")
                continue

            # 将字符串 ID 转换为 UUID 格式
            point_id = doc.id
            # 检查是否是有效的 UUID，如果不是则生成一个新的 UUID
            try:
                uuid.UUID(point_id)
            except ValueError:
                # 生成基于 doc.id 的确定性 UUID
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.id))
                logger.debug(f"Converted chunk ID {doc.id} to UUID {point_id}")

            point = models.PointStruct(
                id=point_id,
                vector=doc.vector.tolist() if isinstance(doc.vector, np.ndarray) else doc.vector,
                payload={
                    "content": doc.content,
                    "metadata": doc.metadata,
                    "original_id": doc.id,  # 保存原始 ID 用于追溯
                },
            )
            points.append(point)

        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            logger.info(f"Added {len(points)} documents to Qdrant")

        return True

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[SearchResult]:
        """向量检索"""
        self.ensure_collection()

        from qdrant_client.http import models

        query_filter = None
        if filter_dict:
            must = []
            for key, value in filter_dict.items():
                must.append(models.FieldCondition(
                    key=f"metadata.{key}",
                    match=models.MatchValue(value=value),
                ))
            query_filter = models.Filter(must=must)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist() if isinstance(query_vector, np.ndarray) else query_vector,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        )

        search_results = []
        for hit in results.points:
            payload = hit.payload or {}
            search_results.append(SearchResult(
                id=str(hit.id),
                content=payload.get("content", ""),
                score=hit.score,
                metadata=payload.get("metadata", {}),
                parent_id=payload.get("metadata", {}).get("parent_id"),
                is_parent=payload.get("metadata", {}).get("is_parent", False),
            ))

        return search_results

    def search_by_text(
        self,
        query_text: str,
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[SearchResult]:
        """文本检索（需要外部编码）"""
        raise NotImplementedError("Use search() with pre-computed query vector")

    def delete(self, doc_ids: List[str]) -> bool:
        """删除文档"""
        if not doc_ids:
            return True

        from qdrant_client.http import models
        import uuid

        # 转换字符串 ID 为 UUID 格式
        point_ids = []
        for doc_id in doc_ids:
            try:
                uuid.UUID(doc_id)
                point_ids.append(doc_id)
            except ValueError:
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_id))
                point_ids.append(point_id)

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=point_ids,
            ),
        )
        logger.info(f"Deleted {len(doc_ids)} documents from Qdrant")
        return True

    def count(self) -> int:
        """统计文档数量"""
        try:
            result = self.client.get_collection(self.collection_name)
            return result.points_count
        except:
            return 0

    def clear(self) -> bool:
        """清空集合"""
        try:
            self.client.delete_collection(self.collection_name)
            self._collection_ready = False
            logger.info(f"Cleared collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            return False


class ChromaStore(VectorStore):
    """
    ChromaDB 向量数据库

    轻量级本地向量数据库，适合开发测试
    """

    def __init__(
        self,
        collection_name: str = "knowledge_base",
        vector_dim: int = 1024,
        persist_directory: Optional[str] = None,
    ):
        self.collection_name = collection_name
        self.vector_dim = vector_dim
        self.persist_directory = persist_directory
        self._client = None
        self._collection = None

    @property
    def client(self):
        """懒加载客户端"""
        if self._client is None:
            try:
                import chromadb
                from chromadb.config import Settings

                settings = Settings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                )

                if self.persist_directory:
                    self._client = chromadb.PersistentClient(
                        path=self.persist_directory,
                        settings=settings,
                    )
                else:
                    self._client = chromadb.Client(settings=settings)

            except ImportError:
                raise ImportError("请安装 chromadb: pip install chromadb")

        return self._client

    @property
    def collection(self):
        """获取或创建 Collection"""
        if self._collection is None:
            try:
                self._collection = self.client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"dimension": self.vector_dim},
                )
            except Exception as e:
                logger.error(f"Failed to get collection: {e}")
                raise
        return self._collection

    def add(self, documents: List[Document]) -> bool:
        """添加文档到 ChromaDB"""
        if not documents:
            return True

        ids = [doc.id for doc in documents]
        contents = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        vectors = []
        for doc in documents:
            if doc.vector is None:
                logger.warning(f"Document {doc.id} has no vector")
                vectors.append([0.0] * self.vector_dim)
            else:
                vectors.append(doc.vector.tolist() if isinstance(doc.vector, np.ndarray) else doc.vector)

        self.collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas,
            embeddings=vectors,
        )

        logger.info(f"Added {len(documents)} documents to ChromaDB")
        return True

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[SearchResult]:
        """向量检索"""
        where = None
        if filter_dict:
            where = filter_dict

        results = self.collection.query(
            query_embeddings=[query_vector.tolist() if isinstance(query_vector, np.ndarray) else query_vector],
            n_results=top_k,
            where=where,
            include=["metadatas", "distances", "documents"],
        )

        search_results = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                search_results.append(SearchResult(
                    id=doc_id,
                    content=results["documents"][0][i] if results.get("documents") else "",
                    score=1 - results["distances"][0][i] if results.get("distances") else 0.0,
                    metadata=results["metadatas"][0][i] if results.get("metadatas") else {},
                    parent_id=results["metadatas"][0][i].get("parent_id") if results.get("metadatas") else None,
                    is_parent=results["metadatas"][0][i].get("is_parent", False) if results.get("metadatas") else False,
                ))

        return search_results

    def delete(self, doc_ids: List[str]) -> bool:
        """删除文档"""
        if doc_ids:
            self.collection.delete(ids=doc_ids)
            logger.info(f"Deleted {len(doc_ids)} documents from ChromaDB")
        return True

    def count(self) -> int:
        """统计文档数量"""
        return self.collection.count()

    def clear(self) -> bool:
        """清空 Collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self._collection = None
            logger.info(f"Cleared collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            return False


class FileVectorStore(VectorStore):
    """
    基于 JSON 文件的简单向量存储

    用于无数据库环境下的开发和测试
    """

    def __init__(self, storage_path: str = "./data/vectors_store.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        """从文件加载数据"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)

    def _save(self):
        """保存数据到文件"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def add(self, documents: List[Document]) -> bool:
        """添加文档"""
        for doc in documents:
            self._data[doc.id] = {
                "content": doc.content,
                "vector": doc.vector.tolist() if isinstance(doc.vector, np.ndarray) else doc.vector,
                "metadata": doc.metadata,
            }
        self._save()
        return True

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        filter_dict: Optional[Dict] = None,
    ) -> List[SearchResult]:
        """向量检索（余弦相似度）"""
        if not self._data:
            return []

        qv = np.array(query_vector)
        results = []

        for doc_id, doc_data in self._data.items():
            if filter_dict:
                metadata = doc_data.get("metadata", {})
                if not all(metadata.get(k) == v for k, v in filter_dict.items()):
                    continue

            vec = np.array(doc_data["vector"])
            score = float(np.dot(qv, vec) / (np.linalg.norm(qv) * np.linalg.norm(vec) + 1e-10))

            results.append(SearchResult(
                id=doc_id,
                content=doc_data["content"],
                score=score,
                metadata=doc_data.get("metadata", {}),
                parent_id=doc_data.get("metadata", {}).get("parent_id"),
                is_parent=doc_data.get("metadata", {}).get("is_parent", False),
            ))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def delete(self, doc_ids: List[str]) -> bool:
        """删除文档"""
        for doc_id in doc_ids:
            self._data.pop(doc_id, None)
        self._save()
        return True

    def count(self) -> int:
        """统计文档数量"""
        return len(self._data)

    def clear(self) -> bool:
        """清空存储"""
        self._data = {}
        self._save()
        return True


def create_vector_store(
    store_type: str = "chroma",
    collection_name: str = "knowledge_base",
    vector_dim: int = 1024,
    persist_directory: Optional[str] = None,
    **kwargs,
) -> VectorStore:
    """
    创建向量存储实例

    Args:
        store_type: 存储类型 (qdrant/chroma/file)
        collection_name: Collection 名称
        vector_dim: 向量维度
        persist_directory: 持久化目录

    Returns:
        VectorStore 实例
    """
    if store_type == "qdrant":
        return QdrantStore(
            collection_name=collection_name,
            vector_dim=vector_dim,
            host=kwargs.get("host", "localhost"),
            port=kwargs.get("port", 6333),
            grpc_port=kwargs.get("grpc_port", 6334),
        )
    elif store_type == "chroma":
        return ChromaStore(
            collection_name=collection_name,
            vector_dim=vector_dim,
            persist_directory=persist_directory,
        )
    elif store_type == "file":
        return FileVectorStore(
            storage_path=persist_directory or "./data/vectors_store.json",
        )
    else:
        raise ValueError(f"Unknown store type: {store_type}")


# 全局实例
_default_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """获取全局向量存储"""
    global _default_store
    if _default_store is None:
        from config.settings import settings
        _default_store = create_vector_store(
            store_type=settings.VECTOR_DB_TYPE,
            collection_name=settings.QDRANT_COLLECTION,
            vector_dim=settings.VECTOR_DIM,
            persist_directory=str(settings.VECTOR_DIR),
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            grpc_port=settings.QDRANT_GRPC_PORT,
        )
    return _default_store
