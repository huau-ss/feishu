"""
RAG 核心引擎
实现：文档处理 → 向量检索 → Reranker → LLM 生成
"""
import logging
import time
import json
from typing import List, Dict, Optional, Any, Generator, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np

from parsers import extract, ParserFactory
from parsers.data_cleaner import clean, DataCleaner, CleanResult
from core.chunker import chunk, ParentChildChunker, ChunkingResult, TextChunk, DocType, AutoTagger, extract_query_keywords
from core.embedding import encode, encode_query, get_embedding_model, EmbeddingModel
from core.reranker import rerank, get_reranker, RerankerModel, BGEReranker
from vectorstore import Document, get_vector_store, VectorStore, SearchResult
from storage import get_document_storage, DocumentStorage
from llm import ChatMessage, LLMResponse, get_llm_client, BaseLLMClient, create_llm_client

logger = logging.getLogger(__name__)


@dataclass
class RAGResult:
    """RAG 查询结果"""
    answer: str
    answer_source: str = ""  # "knowledge_base" | "external_llm" | "none"
    sources: List[Dict[str, Any]] = field(default_factory=list)
    query: str = ""
    retrieved_chunks: int = 0
    reranked_chunks: int = 0
    used_chunks: int = 0
    from_knowledge_base: bool = False
    latency_ms: float = 0.0
    model: str = ""
    metadata: Dict = field(default_factory=dict)


class RAGEngine:
    """
    RAG 核心引擎

    流程：
    1. 文档处理：解析 → 清洗 → 分片
    2. 向量化和存储：Embedding → Vector Store
    3. 查询：向量检索 → Reranker → LLM 生成
    4. 混合查询：知识库查询 + 公网大模型
    """

    SYSTEM_PROMPT = """你是一个专业的知识库问答助手。你的任务是：
1. 基于提供的参考资料回答用户问题
2. 如果参考资料包含相关信息，给出准确、详细的回答
3. 如果参考资料不包含答案，坦诚告知用户
4. 回答要基于事实，引用参考资料时要标注来源

参考资料将以特定格式提供，格式为：
---
来源: [文档标题]
内容: [文档内容]
---

请根据参考资料回答问题。"""

    def __init__(
        self,
        embedding_model: EmbeddingModel = None,
        reranker: RerankerModel = None,
        vector_store: VectorStore = None,
        document_storage: DocumentStorage = None,
        llm_client: BaseLLMClient = None,
        external_llm_client: BaseLLMClient = None,
        chunker: ParentChildChunker = None,
        cleaner: DataCleaner = None,
        top_k: int = 20,
        rerank_top_k: int = 10,
        rerank_threshold: float = 0.5,
        max_context_chunks: int = 5,
    ):
        self.embedding_model = embedding_model or get_embedding_model()
        self.reranker = reranker or get_reranker()
        self.vector_store = vector_store or get_vector_store()
        self.document_storage = document_storage or get_document_storage()
        self.llm_client = llm_client
        self.external_llm_client = external_llm_client
        self.chunker = chunker or ParentChildChunker()
        self.cleaner = cleaner or DataCleaner()

        self.top_k = top_k
        self.rerank_top_k = rerank_top_k
        self.rerank_threshold = rerank_threshold
        self.max_context_chunks = max_context_chunks

    def set_llm_client(self, client: BaseLLMClient):
        """设置 LLM 客户端（本地 Ollama）"""
        self.llm_client = client

    def set_external_llm_client(self, client: BaseLLMClient):
        """设置外部 LLM 客户端（公网大模型）"""
        self.external_llm_client = client

    def _get_active_llm_client(self, use_external: bool) -> BaseLLMClient:
        """获取当前使用的 LLM 客户端"""
        if use_external and self.external_llm_client:
            return self.external_llm_client
        return self.llm_client

    def _resolve_doc_type(self, doc_type_str: str) -> Optional[DocType]:
        """将清洗器返回的 doc_type 字符串映射为 DocType 枚举"""
        mapping = {
            "article": DocType.ARTICLE,
            "spec_sheet": DocType.SPREADSHEET,
            "price_list": DocType.SPREADSHEET,
            "config_file": DocType.CONFIG,
            "notes": DocType.NOTES,
        }
        return mapping.get(doc_type_str, DocType.ARTICLE)

    def _build_personalized_prompt(
        self,
        system_template: str,
        query_keywords: List[str],
        matched_tags: List[str],
    ) -> str:
        """
        根据用户查询关键字构建个性化提示词

        Args:
            system_template: 系统提示词模板
            query_keywords: 查询中提取的关键字
            matched_tags: 与查询匹配的文档标签

        Returns:
            个性化的系统提示词
        """
        personalization = ""

        if matched_tags:
            # 根据匹配的标签调整回答风格
            style_hints = {
                "运维": "回答要注重操作步骤的清晰性和可执行性，包含具体的命令和配置示例。",
                "部署": "回答要包含详细的部署流程、环境要求和注意事项。",
                "产品": "回答要注重产品特性、规格参数和选型建议，条理清晰。",
                "开发": "回答要包含技术原理、代码示例和最佳实践。",
                "安全": "回答要强调安全风险、防护措施和合规要求。",
                "数据库": "回答要包含具体的SQL语句、表结构设计和优化建议。",
                "财务": "回答要注重数据的准确性，提供清晰的费用明细和计费逻辑。",
                "技术支持": "回答要结构化，优先给出解决步骤，必要时给出排查路径。",
            }
            active_hints = [style_hints.get(tag, "") for tag in matched_tags if tag in style_hints]
            if active_hints:
                personalization = "\n".join(active_hints)

        if personalization:
            return f"{system_template.strip()}\n\n补充要求：{personalization}"
        return system_template

    def process_document(
        self,
        file_path: str | Path,
        metadata: Dict = None,
        save_cleaned: bool = True,
    ) -> Dict[str, Any]:
        """
        处理单个文档

        流程：解析 → 清洗 → (保存) → 分片 → 向量化 → 存储

        Args:
            file_path: 文件路径
            metadata: 额外元数据
            save_cleaned: 是否保存清洗后的文档到本地文件

        Returns:
            处理结果统计
        """
        start_time = time.time()
        file_path = Path(file_path)
        metadata = metadata or {}

        logger.info(f"Processing document: {file_path.name}")

        try:
            file_type = file_path.suffix.lower().lstrip('.')

            record = self.document_storage.add(
                title=file_path.stem,
                file_path=str(file_path),
                file_type=file_type,
                file_size=file_path.stat().st_size,
                metadata=metadata,
            )
            doc_id = record.doc_id

            self.document_storage.update_status(doc_id, "indexing")
            self.vector_store.ensure_collection()

            # 1. 解析
            text = extract(file_path)
            logger.info(f"Extracted {len(text)} characters")

            # 2. 清洗
            clean_result = self.cleaner.clean(text, filename=file_path.name, file_type=file_type)
            logger.info(f"Cleaned: type={clean_result.doc_type}")

            # 3. (可选) 保存清洗后的文档到本地
            if save_cleaned:
                cleaned_doc_path = self._save_cleaned_document(
                    doc_id=doc_id,
                    file_path=str(file_path),
                    clean_result=clean_result,
                    metadata=metadata,
                )
                logger.info(f"Saved cleaned document to: {cleaned_doc_path}")

            # 4. 分片（传入 doc_type 选择最优策略）
            # 注意：metadata 放在前面，用户传入的值会覆盖默认值
            merged_metadata = {
                "doc_type": clean_result.doc_type,
                "pdf_type": clean_result.metadata.get("pdf_type"),
                **metadata,  # 用户传入的 tags 等优先
            }
            # 如果用户没有提供 tags，则自动提取
            if "tags" not in merged_metadata or not merged_metadata["tags"]:
                merged_metadata["tags"] = clean_result.metadata.get("tags", [])
            
            logger.info(f"Chunking metadata: doc_id={doc_id}, tags={merged_metadata.get('tags')}")

            chunking_result = self.chunker.chunk(
                clean_result.content,
                doc_id=doc_id,
                title=clean_result.title,
                metadata=merged_metadata,
                doc_type=self._resolve_doc_type(clean_result.doc_type),
            )

            all_chunks = chunking_result.parent_chunks + chunking_result.child_chunks
            logger.info(f"Chunked: {len(chunking_result.parent_chunks)} parent, {len(chunking_result.child_chunks)} child")

            # 5. 向量化
            texts_to_embed = [chunk.content for chunk in all_chunks]
            embeddings = self.embedding_model.encode(texts_to_embed)

            # 6. 存储到向量数据库
            documents = []
            for i, chunk in enumerate(all_chunks):
                doc = Document(
                    id=chunk.chunk_id,
                    content=chunk.content,
                    vector=embeddings[i],
                    metadata={
                        "doc_id": doc_id,
                        "title": clean_result.title,
                        "doc_type": clean_result.doc_type,
                        "is_parent": chunk.is_parent,
                        "parent_id": chunk.parent_id,
                        "chunk_index": chunk.chunk_index,
                        **chunk.metadata,
                    },
                )
                documents.append(doc)

            self.vector_store.add(documents)

            self.document_storage.update_status(
                doc_id,
                "indexed",
                chunk_count=len(all_chunks),
            )

            elapsed = time.time() - start_time
            logger.info(f"Document {doc_id} indexed in {elapsed:.2f}s")

            return {
                "doc_id": doc_id,
                "title": clean_result.title,
                "doc_type": clean_result.doc_type,
                "parent_chunks": len(chunking_result.parent_chunks),
                "child_chunks": len(chunking_result.child_chunks),
                "total_chunks": len(all_chunks),
                "total_chars": chunking_result.total_chars,
                "elapsed_seconds": elapsed,
                "cleaned_file": str(self._get_cleaned_path(doc_id)) if save_cleaned else None,
            }

        except Exception as e:
            logger.error(f"Failed to process document {file_path}: {e}")
            raise

    def _get_cleaned_path(self, doc_id: str) -> Path:
        """获取清洗后文档的存储路径"""
        from config import settings
        cleaned_dir = settings.CLEANED_DIR
        cleaned_dir.mkdir(parents=True, exist_ok=True)
        return cleaned_dir / f"{doc_id}.md"

    def _save_cleaned_document(
        self,
        doc_id: str,
        file_path: str,
        clean_result,
        metadata: Dict = None,
    ) -> Path:
        """保存清洗后的文档为 Markdown 格式"""
        from datetime import datetime

        cleaned_path = self._get_cleaned_path(doc_id)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_type = Path(file_path).suffix.lower().lstrip('.')

        lines = []

        tags = []
        meta = clean_result.metadata or {}
        if meta:
            tags = meta.get("tags", [])
        merged_tags = tags
        if metadata and "tags" in metadata:
            merged_tags = metadata["tags"]

        frontmatter = [
            "---",
            f"title: \"{clean_result.title}\"",
            f"doc_id: \"{doc_id}\"",
            f"source_file: \"{file_path}\"",
            f"file_type: \"{file_type}\"",
            f"doc_type: \"{clean_result.doc_type}\"",
            f"cleaned_at: \"{created_at}\"",
        ]
        if merged_tags:
            tag_str = ", ".join(f'"{t}"' for t in merged_tags)
            frontmatter.append(f"tags: [{tag_str}]")
        frontmatter.append("---")
        lines.extend(frontmatter)

        lines.append("")
        lines.append(f"# {clean_result.title}")
        lines.append("")

        lines.append("## 基本信息")
        lines.append("")
        lines.append(f"| 字段 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| 文档ID | `{doc_id}` |")
        lines.append(f"| 来源文件 | `{file_path}` |")
        lines.append(f"| 文件类型 | `{file_type}` |")
        lines.append(f"| 文档类型 | `{clean_result.doc_type}` |")
        lines.append(f"| 清洗时间 | `{created_at}` |")

        warnings = clean_result.warnings or []
        if warnings:
            lines.append("")
            lines.append("## 清洗警告")
            lines.append("")
            for w in warnings:
                lines.append(f"- {w}")

        if meta:
            key_meta_items = [(k, v) for k, v in meta.items()
                               if k not in ("key_values", "tables", "tags", "pdf_type", "format", "row_count")]
            if key_meta_items:
                lines.append("")
                lines.append("## 元数据")
                lines.append("")
                lines.append("| 字段 | 值 |")
                lines.append("|------|-----|")
                for k, v in key_meta_items:
                    v_str = str(v)[:200]
                    lines.append(f"| {k} | {v_str} |")

            if "key_values" in meta and isinstance(meta["key_values"], dict) and meta["key_values"]:
                lines.append("")
                lines.append("## 关键字段")
                lines.append("")
                lines.append("| 字段 | 值 |")
                lines.append("|------|-----|")
                for kv, vv in list(meta["key_values"].items())[:30]:
                    lines.append(f"| {kv} | {vv} |")

            if "tables" in meta and isinstance(meta["tables"], list) and meta["tables"]:
                lines.append("")
                lines.append("## 表格数据")
                for i, tbl in enumerate(meta["tables"][:5]):
                    if isinstance(tbl, list) and tbl:
                        lines.append("")
                        lines.append(f"### 表格 {i + 1}")
                        lines.append("")
                        if tbl[0]:
                            lines.append("| " + " | ".join(str(c) for c in tbl[0]) + " |")
                            lines.append("| " + " | ".join("---" for _ in tbl[0]) + " |")
                        for row in tbl[1:]:
                            lines.append("| " + " | ".join(str(c) for c in row) + " |")

        if merged_tags:
            lines.append("")
            lines.append("## 标签")
            lines.append("")
            for tag in merged_tags:
                lines.append(f"- `{tag}`")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 正文")
        lines.append("")

        body = clean_result.content or ""
        lines.append(body)

        with open(cleaned_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        return cleaned_path

    def process_directory(
        self,
        directory: str | Path,
        recursive: bool = True,
        extensions: List[str] = None,
        max_files: int = None,
        save_cleaned: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        批量处理目录中的文档

        Args:
            directory: 目录路径
            recursive: 是否递归子目录
            extensions: 过滤的文件扩展名
            max_files: 最大处理文件数
            save_cleaned: 是否保存清洗后的文档到本地文件

        Returns:
            处理结果列表
        """
        directory = Path(directory)
        parser = ParserFactory()

        if extensions:
            extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
                         for ext in extensions]
        else:
            extensions = parser.supported_extensions()

        patterns = ["**/*" if recursive else "*"]
        files = []
        for pattern in patterns:
            for ext in extensions:
                files.extend(directory.glob(f"{pattern}{ext}"))

        files = list(set(files))
        if max_files:
            files = files[:max_files]

        logger.info(f"Found {len(files)} files to process in {directory}")

        results = []
        for i, file_path in enumerate(files, 1):
            try:
                logger.info(f"Processing {i}/{len(files)}: {file_path.name}")
                result = self.process_document(file_path, save_cleaned=save_cleaned)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                results.append({
                    "file": str(file_path),
                    "error": str(e),
                })

        return results

    def retrieve(
        self,
        query: str,
        top_k: int = None,
        filter_dict: Dict = None,
    ) -> List[SearchResult]:
        """
        检索相关文档

        Args:
            query: 查询文本
            top_k: 召回数量
            filter_dict: 过滤条件

        Returns:
            检索结果列表
        """
        if top_k is None:
            top_k = self.top_k

        query_vector = self.embedding_model.encode_query(query)

        results = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            filter_dict=filter_dict,
        )

        return results

    def rerank_chunks(
        self,
        query: str,
        chunks: List[SearchResult],
    ) -> List[SearchResult]:
        """
        重排文档块

        Args:
            query: 查询文本
            chunks: 检索结果

        Returns:
            重排后的结果
        """
        if not chunks:
            return []

        contents = [chunk.content for chunk in chunks]

        try:
            reranked = self.reranker.rerank(query, contents, top_k=self.rerank_top_k)
            scores = {idx: score for idx, score in reranked}

            reranked_chunks = []
            for i, chunk in enumerate(chunks):
                if i in scores and scores[i] >= self.rerank_threshold:
                    chunk.score = scores[i]
                    reranked_chunks.append(chunk)
                elif i in scores:
                    chunk.score = scores[i]

            reranked_chunks.sort(key=lambda x: x.score, reverse=True)
            return reranked_chunks

        except Exception as e:
            logger.error(f"Reranker failed: {e}")
            return chunks[:self.rerank_top_k]

    def get_parent_chunks(
        self,
        child_chunks: List[SearchResult],
    ) -> List[SearchResult]:
        """
        获取父文档块（去重）

        从子文档块中提取父文档，同一父文档下的多个子文档只保留得分最高的
        """
        parent_map: Dict[str, SearchResult] = {}
        parent_scores: Dict[str, float] = {}

        for chunk in child_chunks:
            parent_id = chunk.metadata.get("parent_id") or chunk.id

            if parent_id not in parent_scores or chunk.score > parent_scores[parent_id]:
                parent_scores[parent_id] = chunk.score
                parent_map[parent_id] = SearchResult(
                    id=parent_id,
                    content=chunk.metadata.get("parent_content", chunk.content),
                    score=chunk.score,
                    metadata=chunk.metadata,
                )

        parents = list(parent_map.values())
        parents.sort(key=lambda x: x.score, reverse=True)
        return parents[:self.max_context_chunks]

    def build_context(
        self,
        chunks: List[SearchResult],
    ) -> str:
        """构建上下文"""
        context_parts = []

        for i, chunk in enumerate(chunks, 1):
            title = chunk.metadata.get("title", "未知文档")
            context_parts.append(
                f"--- 参考资料 {i} ---\n"
                f"来源: {title}\n"
                f"内容: {chunk.content[:500]}..."
            )

        return "\n\n".join(context_parts)

    def query(
        self,
        question: str,
        use_knowledge_base: bool = True,
        use_external_llm: bool = True,
        session_id: str = None,
    ) -> RAGResult:
        """
        RAG 查询（知识库优先 + 公网兜底）

        模式：
        - 知识库有结果 → 本地 LLM 基于 KB 上下文回答
        - 知识库无结果 + use_external_llm=True → 公网 LLM 兜底
        - 知识库无结果 + use_external_llm=False → 诚实回答无法给出答案
        - use_knowledge_base=False → 完全走公网大模型

        Args:
            question: 用户问题
            use_knowledge_base: 是否使用知识库检索（本地 LLM）
            use_external_llm: 知识库无结果时是否使用公网大模型兜底
            session_id: 会话 ID（用于历史上下文）

        Returns:
            RAGResult: 查询结果
        """
        start_time = time.time()
        result = RAGResult(query=question)

        if not self.llm_client:
            raise ValueError("LLM client not set. Call set_llm_client() first.")

        # 1. 提取查询关键字（用于 Tag 匹配和重排 Boost）
        query_keywords = extract_query_keywords(question, max_keywords=5)
        logger.debug(f"Query keywords: {query_keywords}")
        result.metadata["query_keywords"] = query_keywords

        context_messages = []
        retrieved_chunks = []
        from_kb = False
        matched_tags: List[str] = []

        # ====== 知识库路径：检索 + 本地 LLM ======
        if use_knowledge_base:
            retrieved = self.retrieve(question)
            result.retrieved_chunks = len(retrieved)

            if retrieved:
                reranked = self.rerank_chunks_with_tags(question, retrieved, query_keywords)

                if reranked:
                    parents = self.get_parent_chunks(reranked)
                    result.used_chunks = len(parents)
                    retrieved_chunks = parents
                    from_kb = True

                    all_tags: List[str] = []
                    for chunk in parents:
                        all_tags.extend(chunk.metadata.get("tags", []))
                    from collections import Counter
                    tag_counts = Counter(all_tags)
                    matched_tags = [t for t, _ in tag_counts.most_common(3)]
                    result.metadata["matched_tags"] = matched_tags

                    context = self.build_context(parents)
                    context_messages.append(
                        ChatMessage(role="user", content=f"参考资料:\n{context}\n\n请根据以上参考资料回答问题。")
                    )

        # ====== 决策：走哪条路径 ======
        if from_kb:
            # 路径 A：知识库有结果，本地 LLM 回答
            result.answer_source = "knowledge_base"
        elif not use_knowledge_base and use_external_llm and self.external_llm_client:
            # 路径 B：完全关闭知识库，走公网独立问答
            result.answer_source = "external_llm"
            result.metadata["external_llm_used"] = True
        elif use_knowledge_base and not from_kb and use_external_llm and self.external_llm_client:
            # 路径 C：知识库无结果，公网 LLM 兜底
            result.answer_source = "external_llm"
            result.metadata["external_llm_used"] = True
            logger.info("No relevant chunks found, using external LLM")
        else:
            # 路径 D：无法回答
            result.answer_source = "none"
            result.answer = "抱歉，知识库中没有找到相关答案，同时公网大模型已关闭，无法回答您的问题。"
            result.latency_ms = (time.time() - start_time) * 1000
            return result

        # ====== 构建消息并生成回答 ======
        user_message = ChatMessage(role="user", content=question)
        personalized_system = self._build_personalized_prompt(
            self.SYSTEM_PROMPT, query_keywords, matched_tags
        )
        messages = [ChatMessage(role="system", content=personalized_system)]
        messages.extend(context_messages)
        messages.append(user_message)

        active_llm = self._get_active_llm_client(
            use_external=(result.answer_source == "external_llm")
        )

        response = active_llm.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
        )

        result.answer = response.content
        result.from_knowledge_base = from_kb
        result.latency_ms = (time.time() - start_time) * 1000
        result.model = active_llm.model

        if retrieved_chunks:
            result.sources = [
                {
                    "title": chunk.metadata.get("title", "未知"),
                    "content": chunk.content[:200],
                    "score": chunk.score,
                    "tags": chunk.metadata.get("tags", []),
                }
                for chunk in retrieved_chunks
            ]

        return result

    def rerank_chunks_with_tags(
        self,
        query: str,
        chunks: List[SearchResult],
        query_keywords: List[str],
        tag_boost_weight: float = 0.3,
    ) -> List[SearchResult]:
        """
        Tag-Boosted 重排：Reranker 分数 + 关键字 Tag 匹配分数加权

        策略：
        - 先调用 Reranker 获取语义相关性分数
        - 对包含查询关键字的块给予 Tag Boost
        - 合并两个分数进行最终排序

        Args:
            query: 查询文本
            chunks: 检索结果
            query_keywords: 从查询中提取的关键字
            tag_boost_weight: Tag 匹配分数的权重

        Returns:
            重排后的结果
        """
        if not chunks:
            return []

        # 1. 先做 Reranker 重排
        contents = [chunk.content for chunk in chunks]
        try:
            reranked = self.reranker.rerank(query, contents, top_k=self.rerank_top_k)
            scores = {idx: score for idx, score in reranked}
        except Exception as e:
            logger.error(f"Reranker failed: {e}")
            scores = {i: chunk.score for i, chunk in enumerate(chunks)}

        # 2. 计算 Tag Boost 分数
        query_lower = query.lower()
        keyword_set = set(w.lower() for w in query_keywords)

        boosted_scores: List[float] = []
        for i, chunk in enumerate(chunks):
            base_score = scores.get(i, chunk.score)

            # 块内容的标签与查询关键字的匹配度
            content_lower = chunk.content.lower()
            chunk_tags: List[str] = chunk.metadata.get("tags", [])

            # 分数加成：
            # - 查询关键字在块内容中出现
            keyword_hits = sum(1 for kw in keyword_set if kw in content_lower)
            keyword_boost = min(keyword_hits * 0.05, 0.15)

            # - 块的标签与查询领域匹配
            tag_hits = sum(1 for tag in chunk_tags if tag in query_lower)
            tag_boost = min(tag_hits * 0.1, 0.2)

            boost = keyword_boost + tag_boost
            boosted_score = base_score + (boost * tag_boost_weight)
            boosted_scores.append(boosted_score)

            # 更新 chunk 的分数
            chunk.score = min(boosted_score, 1.0)

        # 3. 按 Boost 后的分数排序
        reranked_chunks = list(chunks)
        reranked_chunks.sort(key=lambda x: x.score, reverse=True)

        # 4. 阈值过滤
        final_chunks = [
            c for c in reranked_chunks
            if c.score >= self.rerank_threshold
        ]

        return final_chunks[:self.rerank_top_k]

    def query_stream(
        self,
        question: str,
        use_knowledge_base: bool = True,
        use_external_llm: bool = True,
        session_id: str = None,
    ) -> Generator[Tuple[str, RAGResult], None, None]:
        """
        流式 RAG 查询（知识库优先 + 公网兜底）

        行为同 query() 方法。

        Yields:
            (token, partial_result)
        """
        start_time = time.time()
        result = RAGResult(answer="", query=question)

        if not self.llm_client:
            raise ValueError("LLM client not set. Call set_llm_client() first.")

        # 1. 提取查询关键字
        query_keywords = extract_query_keywords(question, max_keywords=5)
        result.metadata["query_keywords"] = query_keywords

        context_messages = []
        retrieved_chunks = []
        from_kb = False
        matched_tags: List[str] = []

        # ====== 知识库路径：检索 + 本地 LLM ======
        if use_knowledge_base:
            retrieved = self.retrieve(question)
            result.retrieved_chunks = len(retrieved)

            if retrieved:
                reranked = self.rerank_chunks_with_tags(question, retrieved, query_keywords)
                result.reranked_chunks = len(reranked)

                if reranked:
                    parents = self.get_parent_chunks(reranked)
                    result.used_chunks = len(parents)
                    retrieved_chunks = parents
                    from_kb = True

                    all_tags: List[str] = []
                    for chunk in parents:
                        all_tags.extend(chunk.metadata.get("tags", []))
                    from collections import Counter
                    tag_counts = Counter(all_tags)
                    matched_tags = [t for t, _ in tag_counts.most_common(3)]
                    result.metadata["matched_tags"] = matched_tags

                    context = self.build_context(parents)
                    context_messages.append(
                        ChatMessage(role="user", content=f"参考资料:\n{context}\n\n请根据以上参考资料回答问题。")
                    )

        # ====== 决策：走哪条路径 ======
        logger.info(
            f"Decision: use_kb={use_knowledge_base}, from_kb={from_kb}, "
            f"use_external={use_external_llm}, has_external={bool(self.external_llm_client)}"
        )
        if from_kb:
            # 路径 A：知识库有结果，本地 LLM 回答
            result.answer_source = "knowledge_base"
            logger.info("Path A: Using knowledge base")
        elif not use_knowledge_base and use_external_llm and self.external_llm_client:
            # 路径 B：完全关闭知识库，走公网独立问答
            result.answer_source = "external_llm"
            result.metadata["external_llm_used"] = True
            logger.info("Path B: Using external LLM (KB disabled)")
        elif use_knowledge_base and not from_kb and use_external_llm and self.external_llm_client:
            # 路径 C：知识库无结果，公网 LLM 兜底
            result.answer_source = "external_llm"
            result.metadata["external_llm_used"] = True
            logger.info("Path C: KB empty, falling back to external LLM")
        else:
            # 路径 D：无法回答
            result.answer_source = "none"
            result.answer = "抱歉，知识库中没有找到相关答案，同时公网大模型已关闭，无法回答您的问题。"
            result.latency_ms = (time.time() - start_time) * 1000
            yield "", result
            return

        # 4. 个性化系统提示词
        personalized_system = self._build_personalized_prompt(
            self.SYSTEM_PROMPT, query_keywords, matched_tags
        )
        user_message = ChatMessage(role="user", content=question)
        messages = [ChatMessage(role="system", content=personalized_system)]
        messages.extend(context_messages)
        messages.append(user_message)

        active_llm = self._get_active_llm_client(
            use_external=(result.answer_source == "external_llm")
        )

        full_response = []

        for token in active_llm.stream(
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
        ):
            full_response.append(token)
            result.answer = "".join(full_response)
            result.from_knowledge_base = from_kb
            result.latency_ms = (time.time() - start_time) * 1000
            result.model = active_llm.model
            yield token, result

        # 流结束后补充 sources
        if retrieved_chunks:
            result.sources = [
                {
                    "title": chunk.metadata.get("title", "未知"),
                    "content": chunk.content[:200],
                    "score": chunk.score,
                    "tags": chunk.metadata.get("tags", []),
                }
                for chunk in retrieved_chunks
            ]

    def save_to_knowledge_base(
        self,
        content: str,
        title: str,
        metadata: Dict = None,
    ) -> str:
        """
        将外部大模型返回的内容保存到知识库

        Args:
            content: 内容
            title: 标题
            metadata: 元数据

        Returns:
            文档 ID
        """
        import tempfile

        doc_id = str(uuid.uuid4())
        metadata = metadata or {}

        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8',
        )
        temp_file.write(content)
        temp_file.close()

        try:
            result = self.process_document(temp_file.name, metadata={
                "title": title,
                "source": "external_llm",
                **metadata,
            })
            return result.get("doc_id", doc_id)
        finally:
            Path(temp_file.name).unlink(missing_ok=True)


    def get_cleaned_document(self, doc_id: str) -> Optional[str]:
        """
        获取清洗后的 Markdown 文档内容

        Args:
            doc_id: 文档 ID

        Returns:
            Markdown 内容，None 表示不存在
        """
        cleaned_path = self._get_cleaned_path(doc_id)
        if not cleaned_path.exists():
            return None

        try:
            with open(cleaned_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read cleaned document {doc_id}: {e}")
            return None

    def list_cleaned_documents(self) -> List[Dict]:
        """
        列出所有清洗后的文档

        Returns:
            文档信息列表（不含内容）
        """
        from config import settings

        cleaned_dir = settings.CLEANED_DIR
        if not cleaned_dir.exists():
            return []

        documents = []
        for file_path in cleaned_dir.glob("*.md"):
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                title = lines[0].lstrip('#').strip() if lines else file_path.stem
                size = len(content)
                mtime = file_path.stat().st_mtime
                import time
                created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
                documents.append({
                    "doc_id": file_path.stem,
                    "title": title,
                    "source_file": "",
                    "doc_type": "",
                    "status": "cleaned",
                    "created_at": created_at,
                    "file_size": size,
                })
            except Exception as e:
                logger.warning(f"Failed to read {file_path}: {e}")

        return sorted(documents, key=lambda x: x.get("created_at", ""), reverse=True)

    def delete_cleaned_document(self, doc_id: str) -> bool:
        """
        删除清洗后的文档文件

        Args:
            doc_id: 文档 ID

        Returns:
            是否成功删除
        """
        cleaned_path = self._get_cleaned_path(doc_id)
        if cleaned_path.exists():
            cleaned_path.unlink()
            return True
        return False


# 全局实例
_default_engine: Optional[RAGEngine] = None


def get_rag_engine() -> RAGEngine:
    """获取全局 RAG 引擎"""
    global _default_engine
    if _default_engine is None:
        _default_engine = RAGEngine()
    return _default_engine
