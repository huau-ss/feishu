"""
Reranker 模型模块
使用 FlagEmbedding 进行文档重排序
"""
import logging
from typing import List, Optional, Tuple, Union
import numpy as np

logger = logging.getLogger(__name__)


class RerankerModel:
    """Reranker 模型基类"""

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10,
    ) -> List[Tuple[int, float]]:
        """
        重排序文档

        Args:
            query: 查询文本
            documents: 文档列表
            top_k: 返回前 k 个

        Returns:
            List[(doc_index, score)]: 重排序后的文档索引和得分
        """
        raise NotImplementedError


class BGEReranker(RerankerModel):
    """
    BGE Reranker (基于 FlagEmbedding)

    本地使用 bge-reranker-base 或 bge-reranker-large
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-base",
        device: str = "cpu",
        use_fp16: bool = False,
        cache_dir: Optional[str] = None,
    ):
        """
        Args:
            model_name: 模型名称
            device: 设备 (cpu/cuda)
            use_fp16: 是否使用 FP16
            cache_dir: 模型缓存目录
        """
        self.model_name = model_name
        self.device = device
        self.use_fp16 = use_fp16 and device == "cuda"
        self.cache_dir = cache_dir
        self._model = None

    @property
    def model(self):
        """懒加载模型"""
        if self._model is None:
            try:
                from FlagEmbedding import FlagReranker
                self._model = FlagReranker(
                    self.model_name,
                    use_fp16=self.use_fp16,
                    cache_dir=self.cache_dir,
                )
                logger.info(f"Loaded reranker model: {self.model_name}")
            except ImportError:
                raise ImportError(
                    "请安装 FlagEmbedding: pip install FlagEmbedding"
                )
        return self._model

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10,
    ) -> List[Tuple[int, float]]:
        """使用 BGE Reranker 重排序"""
        if not documents:
            return []

        if len(documents) == 1:
            return [(0, 1.0)]

        try:
            pairs = [[query, doc] for doc in documents]
            scores = self.model.compute_score(pairs, normalize=True)

            if isinstance(scores, float):
                scores = [scores]

            doc_scores = list(zip(range(len(documents)), scores))
            doc_scores.sort(key=lambda x: x[1], reverse=True)

            return doc_scores[:top_k]

        except Exception as e:
            logger.error(f"Reranker failed: {e}")
            return [(i, 1.0 / (i + 1)) for i in range(min(top_k, len(documents)))]


class SimpleReranker(RerankerModel):
    """
    简单 Reranker (基于关键词匹配)

    当 FlagEmbedding 不可用时使用
    """

    def __init__(self, alpha: float = 0.7):
        """
        Args:
            alpha: 相似度权重 (1-alpha 为关键词权重)
        """
        self.alpha = alpha

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10,
        similarity_scores: Optional[List[float]] = None,
    ) -> List[Tuple[int, float]]:
        """使用关键词匹配重排序"""
        if not documents:
            return []

        query_terms = set(query.lower().split())
        scores = []

        for i, doc in enumerate(documents):
            doc_lower = doc.lower()

            keyword_score = 0.0
            for term in query_terms:
                if term in doc_lower:
                    keyword_score += 1.0

            keyword_score = keyword_score / max(len(query_terms), 1)

            base_score = similarity_scores[i] if similarity_scores else (1.0 / (i + 1))

            combined_score = self.alpha * base_score + (1 - self.alpha) * keyword_score
            scores.append(combined_score)

        doc_scores = list(zip(range(len(documents)), scores))
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        return doc_scores[:top_k]


class RemoteReranker(RerankerModel):
    """远程 Reranker (通过 API 调用)"""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        model_name: str = "BAAI/bge-reranker-base",
        api_key: str = "",
    ):
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.api_key = api_key
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import httpx
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.Client(headers=headers, timeout=60.0)
        return self._client

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10,
    ) -> List[Tuple[int, float]]:
        """通过 API 调用远程 Reranker"""
        payload = {
            "query": query,
            "documents": documents,
            "top_k": top_k,
            "model": self.model_name,
        }

        try:
            response = self.client.post(
                f"{self.base_url}/rerank",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

            return [(item["index"], item["score"]) for item in result["results"]]

        except Exception as e:
            logger.error(f"Remote reranker failed: {e}")
            return SimpleReranker().rerank(query, documents, top_k)


class BCEReranker(RerankerModel):
    """
    BCE Reranker (通过海纳数聚 AI 一体机远程调用)
    端点: POST /v1/rerank (Cohere 兼容格式)
    """

    def __init__(
        self,
        base_url: str = "http://192.168.3.86:6006/v1",
        model_name: str = "bce-reranker-base_v1",
        api_key: str = "",
    ):
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.api_key = api_key
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import httpx
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.Client(headers=headers, trust_env=False, timeout=120.0)
        return self._client

    def rerank(
        self,
        query: str,
        documents: List[str],
        top_k: int = 10,
    ) -> List[Tuple[int, float]]:
        """通过 BCE Reranker API 重排序"""
        if not documents:
            return []

        if len(documents) == 1:
            return [(0, 1.0)]

        # Cohere 兼容格式
        payload = {
            "model": self.model_name,
            "query": query,
            "documents": documents,
            "top_n": top_k,
            "return_documents": False,
        }

        try:
            response = self.client.post(
                f"{self.base_url}/rerank",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

            # Cohere 格式: {"results": [{"index": 0, "relevance_score": 0.95}]}
            results = result.get("results", [])
            return [(item["index"], item["relevance_score"]) for item in results]

        except Exception as e:
            logger.warning(f"BCE Reranker /rerank failed: {e}, trying /v1/chat/completions fallback...")

        # Fallback: 尝试用 LLM 风格的 rerank 端点
        try:
            payload = {
                "model": self.model_name,
                "query": query,
                "documents": documents,
                "top_k": top_k,
            }
            response = self.client.post(
                f"{self.base_url}/v1/rerank",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            results = result.get("results", result.get("data", []))
            return [(item.get("index", i), item.get("score", item.get("relevance_score", 0.0))) for i, item in enumerate(results)]

        except Exception as e2:
            logger.error(f"BCE Reranker all endpoints failed: {e2}")
            return SimpleReranker().rerank(query, documents, top_k)


def create_reranker(
    provider: str = "local",
    model_name: str = "BAAI/bge-reranker-base",
    device: str = "cpu",
    base_url: str = "",
    api_key: str = "",
) -> RerankerModel:
    """
    创建 Reranker 实例

    Args:
        provider: 提供商 (local/remote/simple)
        model_name: 模型名称
        device: 设备
        base_url: API 地址
        api_key: API 密钥

    Returns:
        RerankerModel 实例
    """
    if provider == "local":
        return BGEReranker(model_name=model_name, device=device)
    elif provider == "remote":
        return RemoteReranker(base_url=base_url, model_name=model_name, api_key=api_key)
    elif provider == "simple":
        return SimpleReranker()
    else:
        raise ValueError(f"Unknown provider: {provider}")


# 全局实例
_default_reranker: Optional[RerankerModel] = None


def get_reranker() -> RerankerModel:
    """获取全局 Reranker"""
    global _default_reranker
    if _default_reranker is None:
        from config.settings import settings
        # 优先使用海纳数聚一体机 BCE Reranker
        if settings.HAINAN_RERANK_BASE_URL:
            _default_reranker = BCEReranker(
                base_url=settings.HAINAN_RERANK_BASE_URL,
                model_name=settings.HAINAN_RERANK_MODEL,
                api_key=settings.HAINAN_RERANK_API_KEY,
            )
        else:
            _default_reranker = BGEReranker(model_name="BAAI/bge-reranker-base", device="cpu")
    return _default_reranker


def rerank(
    query: str,
    documents: List[str],
    top_k: int = 10,
    similarity_scores: Optional[List[float]] = None,
) -> List[Tuple[int, float]]:
    """便捷函数：重排序文档"""
    return get_reranker().rerank(query, documents, top_k, similarity_scores)
