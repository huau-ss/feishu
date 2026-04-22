"""
本地 RAG Demo 配置
支持本地 Ollama 和外部大模型 API（OpenAI/Claude 等）
"""

import os
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """全局配置"""

    # ==================== 项目路径 ====================
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    STORAGE_DIR: Path = DATA_DIR / "documents"        # 原始文档存储
    CLEANED_DIR: Path = DATA_DIR / "cleaned"           # 清洗后文档
    VECTOR_DIR: Path = DATA_DIR / "vectors"            # 向量数据库

    # ==================== 本地 LLM (Ollama) ====================
    OLLAMA_BASE_URL: str = "http://localhost:8000"
    OLLAMA_MODEL: str = "qwen3-vl:4b"                     # 默认生成模型
    OLLAMA_EMBED_MODEL: str = "bge-m3"                 # 默认嵌入模型

    # ==================== 海纳数聚 AI 一体机 ====================
    # 大语言模型
    HAINAN_LLM_BASE_URL: str = "http://192.168.3.86:18051/v1"
    HAINAN_LLM_MODEL: str = "qwen3_30b_a3b"
    HAINAN_LLM_API_KEY: str = ""

    # 向量嵌入模型
    HAINAN_EMBED_BASE_URL: str = "http://192.168.3.86:6208/v1"
    HAINAN_EMBED_MODEL: str = "bce-embedding-base_v1"
    HAINAN_EMBED_DIM: int = 1536                          # BCE embedding 维度(实测1536)
    HAINAN_EMBED_API_KEY: str = ""

    # 重排模型
    HAINAN_RERANK_BASE_URL: str = "http://192.168.3.86:6006/v1"
    HAINAN_RERANK_MODEL: str = "bce-reranker-base_v1"
    HAINAN_RERANK_API_KEY: str = ""

    # ==================== 外部大模型 API ====================
    EXTERNAL_LLM_PROVIDER: Literal["openai", "claude", "dashscope", "none"] = "openai"
    EXTERNAL_LLM_API_KEY: str = "sk-f5e83e1f3f354048a6232133009b2798"
    EXTERNAL_LLM_BASE_URL: str = "https://api.deepseek.com/v1"
    EXTERNAL_LLM_MODEL: str = "deepseek-chat"

    # DashScope (阿里云通义千问)
    DASHSCOPE_API_KEY: str = ""

    # ==================== RAG 参数 ====================
    VECTOR_DIM: int = 768                                # BCE embedding 向量维度(768)
    TOP_K: int = 20                                     # 粗排召回数量
    RERANK_TOP_K: int = 10                              # 精排后返回数量
    RERANK_THRESHOLD: float = 0.5                       # 重排得分阈值（防幻觉）
    MAX_CONTEXT_CHUNKS: int = 3                         # 最终送入 LLM 的最多块数

    # ==================== 文档处理 ====================
    CHUNK_SIZE: int = 800                               # 子文档块大小（字符）
    CHUNK_OVERLAP: int = 100                            # 块重叠大小
    PARENT_CHUNK_SIZE: int = 2000                       # 父文档大小（字符）
    MAX_FILE_SIZE: int = 50 * 1024 * 1024              # 最大文件 50MB

    # ==================== 对话历史 ====================
    MAX_HISTORY_MESSAGES: int = 20                     # 最大历史消息数
    SESSION_EXPIRE_HOURS: int = 24                      # 会话过期时间（小时）

    # ==================== 服务器配置 ====================
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8001
    STREAMLIT_PORT: int = 8501

    # ==================== HuggingFace 镜像 ====================
    HF_ENDPOINT: str = "https://hf-mirror.com"

    # ==================== 向量数据库 ====================
    VECTOR_DB_TYPE: Literal["qdrant", "chroma"] = "qdrant"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "knowledge_base"
    QDRANT_GRPC_PORT: int = 6334

    # ==================== MySQL 数据库 ====================
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_DATABASE: str = "rag_knowledge_base"
    MYSQL_CHARSET: str = "utf8mb4"

    # ==================== 飞书 Bot 配置 ====================
    FEISHU_APP_ID: str = "cli_a96db55728e45cc4"
    FEISHU_APP_SECRET: str = "DNfJyNRIDPyUj1y6Tw2zRdsToVncETpa"
    FEISHU_VERIFICATION_TOKEN: str = ""
    FEISHU_WEBHOOK_PATH: str = "/feishu/webhook"
    FEISHU_ENABLE_STREAMING: bool = False
    FEISHU_RATE_LIMIT_PER_MINUTE: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()

# 确保 HF_ENDPOINT 被设置到环境变量（供 huggingface_hub 使用）
if settings.HF_ENDPOINT:
    os.environ["HF_ENDPOINT"] = settings.HF_ENDPOINT

# 确保目录存在
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
settings.CLEANED_DIR.mkdir(parents=True, exist_ok=True)
settings.VECTOR_DIR.mkdir(parents=True, exist_ok=True)
