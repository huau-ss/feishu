"""
便捷使用脚本
无需启动服务，直接在 Python 中使用 RAG 功能
"""
import logging
from pathlib import Path
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGDemo:
    """
    本地 RAG Demo 便捷类

    用法:
        rag = RAGDemo()
        rag.process_document("E:/文档/手册.pdf")
        result = rag.query("如何配置网络？")
        print(result.answer)
    """

    def __init__(
        self,
        llm_provider: str = "ollama",
        llm_model: str = "qwen3:4b",
        embed_model: str = "bge-m3",
        ollama_url: str = "http://localhost:11434",
    ):
        from core import get_rag_engine
        from llm import create_llm_client

        logger.info("初始化 RAG Demo...")

        self.rag_engine = get_rag_engine()

        logger.info(f"连接 LLM: {llm_provider}/{llm_model}")
        self.llm_client = create_llm_client(
            provider=llm_provider,
            model=llm_model,
            base_url=ollama_url,
        )
        self.rag_engine.set_llm_client(self.llm_client)

        logger.info("RAG Demo 初始化完成")

    def process_document(self, file_path: str | Path) -> Dict:
        """处理单个文档"""
        return self.rag_engine.process_document(file_path)

    def process_directory(
        self,
        directory: str | Path,
        recursive: bool = True,
        extensions: List[str] = None,
        max_files: int = None,
    ) -> List[Dict]:
        """批量处理目录"""
        return self.rag_engine.process_directory(
            directory, recursive, extensions, max_files
        )

    def query(
        self,
        question: str,
        use_knowledge_base: bool = True,
        use_external_llm: bool = True,
        show_sources: bool = True,
    ) -> Dict:
        """
        查询

        Args:
            question: 问题
            use_knowledge_base: 是否使用知识库
            use_external_llm: 知识库无结果时是否使用外部大模型
            show_sources: 是否显示来源

        Returns:
            {"answer": str, "sources": list, "from_knowledge_base": bool}
        """
        result = self.rag_engine.query(
            question=question,
            use_knowledge_base=use_knowledge_base,
            use_external_llm=use_external_llm,
        )

        response = {
            "answer": result.answer,
            "from_knowledge_base": result.from_knowledge_base,
            "sources": [],
        }

        if show_sources and result.sources:
            print("\n📚 参考来源:")
            for i, source in enumerate(result.sources, 1):
                print(f"  [{i}] {source['title']} (得分: {source['score']:.3f})")
            response["sources"] = result.sources

        return response

    def query_stream(self, question: str, **kwargs):
        """流式查询"""
        for token, result in self.rag_engine.query_stream(question, **kwargs):
            print(token, end="", flush=True)
            yield token

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """搜索相关文档"""
        results = self.rag_engine.retrieve(query, top_k=top_k)
        reranked = self.rag_engine.rerank_chunks(query, results)

        return [
            {
                "content": r.content[:300],
                "score": r.score,
                "title": r.metadata.get("title", "未知"),
            }
            for r in reranked
        ]

    def get_stats(self) -> Dict:
        """获取统计信息"""
        from storage import get_document_storage
        from vectorstore import get_vector_store

        doc_storage = get_document_storage()
        vector_store = get_vector_store()

        return {
            "documents": doc_storage.get_stats(),
            "vectors": {"count": vector_store.count()},
        }

    def clear_all(self):
        """清空所有数据"""
        from storage import get_document_storage
        from vectorstore import get_vector_store

        doc_storage = get_document_storage()
        vector_store = get_vector_store()

        doc_storage.clear_all()
        vector_store.clear()

        logger.info("已清空所有数据")


def quick_demo():
    """快速演示"""
    print("\n" + "=" * 60)
    print("本地 RAG Demo - 快速演示")
    print("=" * 60 + "\n")

    rag = RAGDemo()

    print("\n📁 输入文档路径（或输入 'q' 退出）:")
    while True:
        path = input("\n> ").strip()
        if path.lower() == 'q':
            break

        p = Path(path)
        if not p.exists():
            print(f"❌ 文件不存在: {path}")
            continue

        if p.is_dir():
            print(f"\n📂 处理目录: {path}")
            results = rag.process_directory(p, max_files=10)
            print(f"✅ 处理完成: {len(results)} 个文件")
        else:
            print(f"\n📄 处理文件: {path}")
            result = rag.process_document(p)
            print(f"✅ 处理完成: {result.get('title')}")

    print("\n" + "=" * 60)
    print("文档处理完成，开始问答")
    print("=" * 60 + "\n")

    while True:
        question = input("\n❓ 请输入问题（或输入 'q' 退出）:\n> ").strip()
        if question.lower() == 'q':
            break

        if not question:
            continue

        print("\n🤔 思考中...")
        response = rag.query(question)
        print(f"\n💬 回答:\n{response['answer']}")

    print("\n👋 再见！")


if __name__ == "__main__":
    quick_demo()
