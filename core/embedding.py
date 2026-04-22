"""
Embedding 模型模块
支持本地 Ollama 和外部 API
"""
import logging
from typing import List, Optional, Union
import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """Embedding 模型基类"""

    def __init__(self, model_name: str, dimension: int = 1024):
        self.model_name = model_name
        self.dimension = dimension

    def encode(self, texts: Union[str, List[str]], **kwargs) -> np.ndarray:
        """编码文本为向量"""
        raise NotImplementedError

    def encode_query(self, query: str) -> np.ndarray:
        """编码查询文本"""
        return self.encode([query])[0]


class OllamaEmbedding(EmbeddingModel):
    """Ollama 本地 Embedding"""

    def __init__(
        self,
        model_name: str = "bge-m3",
        base_url: str = "http://localhost:11434",
        dimension: int = 1024,
    ):
        super().__init__(model_name, dimension)
        self.base_url = base_url.rstrip('/')
        self._client = None

    @property
    def client(self):
        """懒加载客户端"""
        if self._client is None:
            import httpx
            self._client = httpx.Client(trust_env=False, timeout=120.0)
        return self._client

    def encode(self, texts: Union[str, List[str]], **kwargs) -> np.ndarray:
        """调用 Ollama API 获取向量"""
        if isinstance(texts, str):
            texts = [texts]

        embeddings = []

        # Ollama /api/embeddings 不支持批量，必须逐个编码
        for text in texts:
            try:
                payload = {
                    "model": self.model_name,
                    "prompt": text,
                }
                response = self.client.post(
                    f"{self.base_url}/api/embeddings",
                    json=payload,
                )
                response.raise_for_status()
                result = response.json()
                embedding = result.get('embedding')
                if not embedding:
                    raise ValueError(f"No embedding in response: {result}")
                embeddings.append(embedding)
            except Exception as e:
                logger.error(f"Failed to encode text: {e}")
                raise

        result = np.array(embeddings)

        if len(result.shape) == 1:
            result = result.reshape(1, -1)

        return result


class OpenAIEmbedding(EmbeddingModel):
    """OpenAI 兼容格式的 Embedding API"""

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        api_key: str = "",
        base_url: str = "https://api.openai.com/v1",
        dimension: int = 1536,
    ):
        super().__init__(model_name, dimension)
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._client = None

        self.dimension_map = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        if model_name in self.dimension_map:
            self.dimension = self.dimension_map[model_name]

    @property
    def client(self):
        """懒加载客户端"""
        if self._client is None:
            import httpx
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.Client(headers=headers, trust_env=False, timeout=60.0)
        return self._client

    def encode(self, texts: Union[str, List[str]], **kwargs) -> np.ndarray:
        """调用 OpenAI 兼容 API 获取向量"""
        if isinstance(texts, str):
            texts = [texts]

        embeddings = []
        batch_size = kwargs.get('batch_size', 100)

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            payload = {
                "model": self.model_name,
                "input": batch,
            }

            response = self.client.post(
                f"{self.base_url}/embeddings",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

            for item in result['data']:
                embeddings.append(item['embedding'])

        return np.array(embeddings)


class DashScopeEmbedding(EmbeddingModel):
    """阿里云 DashScope Embedding"""

    def __init__(
        self,
        model_name: str = "text-embedding-v3",
        api_key: str = "",
        dimension: int = 1024,
    ):
        super().__init__(model_name, dimension)
        self.api_key = api_key

    def encode(self, texts: Union[str, List[str]], **kwargs) -> np.ndarray:
        """调用 DashScope API"""
        import httpx

        if isinstance(texts, str):
            texts = [texts]

        embeddings = []
        batch_size = kwargs.get('batch_size', 25)

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            payload = {
                "model": self.model_name,
                "input": {"texts": batch},
            }

            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = httpx.post(
                "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding",
                json=payload,
                headers=headers,
                timeout=120.0,
            )
            response.raise_for_status()
            result = response.json()

            for item in result['output']['embeddings']:
                embeddings.append(item['embedding'])

        return np.array(embeddings)


class BCEEmbedding(EmbeddingModel):
    """
    BCE (Baidu Chain Embedding) 兼容格式的 Embedding API
    支持海纳数聚 AI 一体机等 OpenAI 兼容接口
    端点: POST /v1/embeddings
    """

    def __init__(
        self,
        model_name: str = "bce-embedding-base_v1",
        api_key: str = "",
        base_url: str = "http://192.168.3.86:6208/v1",
        dimension: int = 768,
    ):
        super().__init__(model_name, dimension)
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._client = None

    @property
    def client(self):
        """懒加载客户端"""
        if self._client is None:
            import httpx
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.Client(headers=headers, trust_env=False, timeout=120.0)
        return self._client

    def encode(self, texts: Union[str, List[str]], **kwargs) -> np.ndarray:
        """调用 BCE Embedding API 获取向量"""
        if isinstance(texts, str):
            texts = [texts]

        embeddings = []
        batch_size = kwargs.get('batch_size', 32)

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            payload = {
                "model": self.model_name,
                "input": batch,
            }

            response = self.client.post(
                f"{self.base_url}/embeddings",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

            for item in result['data']:
                embeddings.append(item['embedding'])

        return np.array(embeddings)


def create_embedding_model(
    provider: str = "ollama",
    model_name: str = "",
    api_key: str = "",
    base_url: str = "",
    dimension: int = 1024,
) -> EmbeddingModel:
    """
    创建 Embedding 模型实例

    Args:
        provider: 提供商 (ollama/openai/dashscope)
        model_name: 模型名称
        api_key: API 密钥
        base_url: API 地址
        dimension: 向量维度

    Returns:
        EmbeddingModel 实例
    """
    if provider == "ollama":
        return OllamaEmbedding(
            model_name=model_name or "bge-m3",
            base_url=base_url or "http://localhost:11434",
            dimension=dimension,
        )
    elif provider == "openai":
        return OpenAIEmbedding(
            model_name=model_name or "text-embedding-3-small",
            api_key=api_key,
            base_url=base_url or "https://api.openai.com/v1",
            dimension=dimension,
        )
    elif provider == "dashscope":
        return DashScopeEmbedding(
            model_name=model_name or "text-embedding-v3",
            api_key=api_key or "",
            dimension=dimension,
        )
    elif provider == "bce":
        return BCEEmbedding(
            model_name=model_name or "bce-embedding-base_v1",
            api_key=api_key,
            base_url=base_url or "http://192.168.3.86:6208/v1",
            dimension=dimension,
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")


# 全局实例
_default_embedding: Optional[EmbeddingModel] = None


def get_embedding_model() -> EmbeddingModel:
    """获取全局 Embedding 模型"""
    global _default_embedding
    if _default_embedding is None:
        from config.settings import settings
        # 优先使用海纳数聚一体机 BCE Embedding
        if settings.HAINAN_EMBED_BASE_URL:
            _default_embedding = BCEEmbedding(
                model_name=settings.HAINAN_EMBED_MODEL,
                api_key=settings.HAINAN_EMBED_API_KEY,
                base_url=settings.HAINAN_EMBED_BASE_URL,
                dimension=settings.HAINAN_EMBED_DIM,
            )
        else:
            _default_embedding = OllamaEmbedding(
                model_name=settings.OLLAMA_EMBED_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                dimension=settings.VECTOR_DIM,
            )
    return _default_embedding


def encode(texts: Union[str, List[str]], **kwargs) -> np.ndarray:
    """便捷函数：编码文本"""
    return get_embedding_model().encode(texts, **kwargs)


def encode_query(query: str) -> np.ndarray:
    """便捷函数：编码查询"""
    return get_embedding_model().encode_query(query)
