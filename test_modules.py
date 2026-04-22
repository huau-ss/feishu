"""
测试脚本
验证各个模块是否正常工作
"""
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_parsers():
    """测试文档解析器"""
    logger.info("=" * 50)
    logger.info("测试 1: 文档解析器")
    logger.info("=" * 50)

    from parsers import get_parser, extract

    parser = get_parser()
    supported = parser.supported_extensions()
    logger.info(f"支持的格式: {', '.join(supported)}")

    test_file = Path("test_data/sample.txt")
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text("这是一个测试文档。RAG 是检索增强生成技术。\n\n它可以帮助大模型获取最新知识。")

    try:
        text = extract(test_file)
        logger.info(f"✅ 解析成功: {len(text)} 字符")
        logger.info(f"   内容预览: {text[:100]}...")
    except Exception as e:
        logger.error(f"❌ 解析失败: {e}")
        return False

    return True


def test_cleaner():
    """测试数据清洗"""
    logger.info("\n" + "=" * 50)
    logger.info("测试 2: 数据清洗")
    logger.info("=" * 50)

    from parsers.data_cleaner import clean

    test_text = """
    这是  一个   测试   文本

    有多余的   空白

    规格表：
    型号：PowerEdge R750xs
    CPU：Intel Xeon
    内存：256GB
    价格：¥50000
    """

    result = clean(test_text, filename="test.txt")

    logger.info(f"✅ 清洗成功")
    logger.info(f"   标题: {result.title}")
    logger.info(f"   类型: {result.doc_type}")
    logger.info(f"   长度: {len(result.content)} 字符")

    return True


def test_chunker():
    """测试分片器"""
    logger.info("\n" + "=" * 50)
    logger.info("测试 3: 父子文档分片")
    logger.info("=" * 50)

    from core.chunker import ParentChildChunker

    test_text = """
    第一章：概述
    RAG（检索增强生成）是一种结合检索和生成的技术。

    第二章：原理
    RAG 通过从外部知识库检索相关文档，增强大模型的回答能力。

    第三章：实现
    典型的 RAG 系统包含以下组件：
    1. 文档解析器
    2. 文本清洗
    3. 向量化
    4. 检索
    5. 重排序
    6. 生成

    第四章：优化
    可以通过以下方式优化 RAG：
    - 使用更好的 Embedding 模型
    - 实施重排序
    - 优化分片策略
    - 使用更好的生成模型
    """

    chunker = ParentChildChunker(chunk_size=200, parent_chunk_size=500)
    result = chunker.chunk(test_text, title="RAG 指南")

    logger.info(f"✅ 分片成功")
    logger.info(f"   父文档数: {len(result.parent_chunks)}")
    logger.info(f"   子文档数: {len(result.child_chunks)}")
    logger.info(f"   总字符数: {result.total_chars}")

    for i, chunk in enumerate(result.parent_chunks[:2], 1):
        logger.info(f"   父文档 {i}: {chunk.content[:50]}...")

    return True


def test_embedding():
    """测试向量化"""
    logger.info("\n" + "=" * 50)
    logger.info("测试 4: 向量化")
    logger.info("=" * 50)

    try:
        from core.embedding import encode

        texts = [
            "什么是 RAG 技术？",
            "RAG 是检索增强生成的缩写",
            "今天天气不错",
        ]

        vectors = encode(texts)

        logger.info(f"✅ 向量化成功")
        logger.info(f"   向量形状: {vectors.shape}")
        logger.info(f"   向量维度: {vectors.shape[1]}")

        import numpy as np
        similarity = np.dot(vectors[0], vectors[1]) / (
            np.linalg.norm(vectors[0]) * np.linalg.norm(vectors[1])
        )
        logger.info(f"   相似度(相关文本): {similarity:.4f}")

        similarity2 = np.dot(vectors[0], vectors[2]) / (
            np.linalg.norm(vectors[0]) * np.linalg.norm(vectors[2])
        )
        logger.info(f"   相似度(不相关文本): {similarity2:.4f}")

        return True

    except Exception as e:
        logger.error(f"❌ 向量化失败: {e}")
        logger.info("   提示: 确保 Ollama 服务已启动并加载 bge-m3 模型")
        return False


def test_vectorstore():
    """测试向量存储"""
    logger.info("\n" + "=" * 50)
    logger.info("测试 5: 向量存储")
    logger.info("=" * 50)

    from vectorstore import create_vector_store, Document
    import numpy as np

    store = create_vector_store("file", persist_directory="./data/test_vectors.json")

    docs = [
        Document(
            id="doc1",
            content="RAG 是检索增强生成技术",
            vector=np.random.rand(1024),
            metadata={"title": "RAG 介绍"},
        ),
        Document(
            id="doc2",
            content="机器学习是人工智能的子领域",
            vector=np.random.rand(1024),
            metadata={"title": "机器学习"},
        ),
    ]

    store.add(docs)
    count = store.count()
    logger.info(f"✅ 存储成功: {count} 个文档")

    results = store.search(np.random.rand(1024), top_k=1)
    logger.info(f"   检索成功: {len(results)} 个结果")

    store.delete(["doc1"])
    count = store.count()
    logger.info(f"   删除后: {count} 个文档")

    store.clear()
    count = store.count()
    logger.info(f"   清空后: {count} 个文档")

    return True


def test_llm():
    """测试 LLM 客户端"""
    logger.info("\n" + "=" * 50)
    logger.info("测试 6: LLM 客户端")
    logger.info("=" * 50)

    try:
        from llm import create_llm_client, ChatMessage

        client = create_llm_client("ollama", model="qwen3:8b")

        messages = [
            ChatMessage(role="user", content="你好，请用一句话介绍 RAG 技术。"),
        ]

        response = client.chat(messages, max_tokens=100)

        logger.info(f"✅ LLM 调用成功")
        logger.info(f"   模型: {response.model}")
        logger.info(f"   回答: {response.content[:200]}...")

        return True

    except Exception as e:
        logger.error(f"❌ LLM 调用失败: {e}")
        logger.info("   提示: 确保 Ollama 服务已启动并加载相应模型")
        return False


def test_history():
    """测试历史管理"""
    logger.info("\n" + "=" * 50)
    logger.info("测试 7: 对话历史")
    logger.info("=" * 50)

    from core.history_manager import HistoryManager
    import time

    manager = HistoryManager(storage_path="./data/test_sessions.json")

    session = manager.create_session(title="测试会话")
    logger.info(f"✅ 创建会话: {session.id}")

    manager.add_message(session.id, "user", "你好")
    manager.add_message(session.id, "assistant", "你好，有什么可以帮助你的？")

    messages = manager.get_messages(session.id)
    logger.info(f"✅ 消息数量: {len(messages)}")

    manager.delete_session(session.id)
    logger.info(f"✅ 删除会话")

    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("本地 RAG Demo - 模块测试")
    print("=" * 60 + "\n")

    tests = [
        ("文档解析器", test_parsers),
        ("数据清洗", test_cleaner),
        ("父子文档分片", test_chunker),
        ("向量化", test_embedding),
        ("向量存储", test_vectorstore),
        ("LLM 客户端", test_llm),
        ("对话历史", test_history),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            logger.error(f"测试 {name} 时发生错误: {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {name}: {status}")

    passed = sum(1 for _, s in results if s)
    print(f"\n通过: {passed}/{len(results)}")

    if passed == len(results):
        print("\n🎉 所有测试通过！可以开始使用 RAG Demo")
    else:
        print("\n⚠️ 部分测试失败，请检查配置和依赖")

    return passed == len(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
