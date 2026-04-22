"""
项目主入口

用法:
    python main.py                 # 启动 Streamlit Web UI
    python main.py --api          # 启动 FastAPI 后端
    python main.py --demo         # 运行演示
    python main.py --feishu-admin # 启动飞书 Bot 管理后台
"""
import sys
import argparse
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="本地 RAG Demo")
    parser.add_argument(
        "--api",
        action="store_true",
        help="启动 FastAPI 后端服务",
    )
    parser.add_argument(
        "--ui",
        action="store_true",
        help="启动 Streamlit Web UI（默认）",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="运行快速演示",
    )
    parser.add_argument(
        "--feishu-admin",
        action="store_true",
        help="启动飞书 Bot 管理后台",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="服务地址（默认: 0.0.0.0）",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Streamlit 端口（默认: 8501）",
    )
    parser.add_argument(
        "--api-port",
        type=int,
        default=8001,
        help="API 端口（默认: 8001）",
    )

    args = parser.parse_args()

    if args.feishu_admin:
        run_feishu_admin(host=args.host, port=args.port)
    elif args.demo:
        run_demo()
    elif args.api:
        run_api(host=args.host, port=args.api_port)
    else:
        run_ui(host=args.host, port=args.port)


def run_ui(host: str = "0.0.0.0", port: int = 8501):
    """启动 Streamlit UI"""
    import subprocess

    logger.info(f"Starting Streamlit UI on {host}:{port}")

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "web_app/app.py",
        "--server.address", host,
        "--server.port", str(port),
        "--browser.gatherUsageStats", "false",
    ]

    subprocess.run(cmd)


def run_api(host: str = "0.0.0.0", port: int = 8001):
    """启动 FastAPI 后端"""
    from api.server import run_server

    logger.info(f"Starting API server on {host}:{port}")
    run_server(host=host, port=port)


def run_feishu_admin(host: str = "0.0.0.0", port: int = 8502):
    """启动飞书 Bot 管理后台"""
    import subprocess

    logger.info(f"Starting Feishu Admin UI on {host}:{port}")

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "feishu/admin_app.py",
        "--server.address", host,
        "--server.port", str(port),
        "--browser.gatherUsageStats", "false",
    ]

    subprocess.run(cmd)


def run_demo():
    """运行快速演示"""
    logger.info("=" * 60)
    logger.info("本地 RAG Demo 快速演示")
    logger.info("=" * 60)

    print("\n" + "=" * 60)
    print("本地 RAG Demo 快速演示")
    print("=" * 60 + "\n")

    print("演示步骤：")
    print("1. 文档处理流程")
    print("2. 向量检索测试")
    print("3. RAG 查询示例\n")

    try:
        from core import get_rag_engine, get_vector_store
        from parsers import extract
        from parsers.data_cleaner import clean
        from core.chunker import ParentChildChunker
        from core.embedding import encode

        print("✅ 模块导入成功\n")

        print("步骤 1: 测试文档解析")
        test_file = Path("demo_test.txt")
        if test_file.exists():
            text = extract(test_file)
            print(f"   - 提取文本: {len(text)} 字符")
        else:
            test_file.write_text("这是一个测试文档。RAG 是检索增强生成技术。")
            text = extract(test_file)
            print(f"   - 创建测试文件并提取: {len(text)} 字符")
        print("   ✅ 文档解析测试完成\n")

        print("步骤 2: 测试文本清洗")
        clean_result = clean(text, filename="demo_test.txt")
        print(f"   - 清洗后长度: {len(clean_result.content)} 字符")
        print(f"   - 文档类型: {clean_result.doc_type}")
        print("   ✅ 文本清洗测试完成\n")

        print("步骤 3: 测试分片")
        chunker = ParentChildChunker()
        chunks = chunker.chunk(clean_result.content, title="Demo Document")
        print(f"   - 父文档数: {len(chunks.parent_chunks)}")
        print(f"   - 子文档数: {len(chunks.child_chunks)}")
        print("   ✅ 分片测试完成\n")

        print("步骤 4: 测试向量化")
        if chunks.child_chunks:
            texts = [c.content for c in chunks.child_chunks]
            vectors = encode(texts)
            print(f"   - 向量维度: {vectors.shape}")
            print("   ✅ 向量化测试完成\n")

        print("=" * 60)
        print("演示完成！")
        print("=" * 60)
        print("\n启动服务命令:")
        print("  Web UI:  python main.py --ui")
        print("  API:     python main.py --api\n")

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("\n请先安装依赖:")
        print("  pip install -r requirements.txt\n")
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
