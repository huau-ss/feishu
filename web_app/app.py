"""
Streamlit Web 应用
提供可视化界面：文档上传、聊天、上下文记忆、历史记录
"""
import streamlit as st
import requests
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Generator
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "http://localhost:8001"

st.set_page_config(
    page_title="ALAN RAG 知识库",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap-gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
    }
    .uploadedFile {
        border: 2px dashed #1E88E5;
        border-radius: 10px;
        padding: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #1E88E5;
    }
    .assistant-message {
        background-color: #F5F5F5;
        border-left: 4px solid #4CAF50;
    }
    .source-box {
        background-color: #FFF8E1;
        border: 1px solid #FFB300;
        border-radius: 5px;
        padding: 0.5rem;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """初始化会话状态"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "chat"
    if "api_connected" not in st.session_state:
        st.session_state.api_connected = False
    if "pending_response" not in st.session_state:
        st.session_state.pending_response = None


def check_api_connection() -> bool:
    """检查 API 连接"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_or_create_session() -> str:
    """获取或创建会话"""
    if not st.session_state.session_id:
        try:
            response = requests.post(
                f"{API_BASE_URL}/sessions",
                json={"title": f"会话 {datetime.now().strftime('%H:%M')}"},
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.session_id = data["id"]
        except Exception as e:
            st.error(f"创建会话失败: {e}")
    return st.session_state.session_id


def send_query(question: str, use_kb: bool = True, use_external: bool = True) -> Dict:
    """发送查询"""
    session_id = get_or_create_session()

    payload = {
        "question": question,
        "session_id": session_id,
        "use_knowledge_base": use_kb,
        "use_external_llm": use_external,
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "请求超时，请稍后重试"}
    except Exception as e:
        return {"error": str(e)}


def send_query_stream(question: str, use_kb: bool = True, use_external: bool = True) -> Generator:
    """流式发送查询"""
    session_id = get_or_create_session()

    payload = {
        "question": question,
        "session_id": session_id,
        "use_knowledge_base": use_kb,
        "use_external_llm": use_external,
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/query/stream",
            json=payload,
            stream=True,
            timeout=300,
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                if line_str.startswith("data: "):
                    data_str = line_str[6:].strip()
                    if data_str and data_str != "[DONE]":
                        try:
                            data = json.loads(data_str)
                            yield data
                        except json.JSONDecodeError:
                            pass
    except Exception as e:
        yield {"error": str(e), "done": True}


def save_to_knowledge_base(question: str, answer: str, tags: List[str] = None) -> Dict:
    """
    保存问答内容到知识库
    
    Args:
        question: 用户问题
        answer: AI 回答
        tags: 标签列表
        
    Returns:
        保存结果
    """
    if not answer or not answer.strip():
        return {"success": False, "error": "回答内容为空"}
    
    tags = tags or ["对话记录", "AI回答"]
    
    payload = {
        "title": f"对话记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "content": f"【用户问题】\n{question}\n\n【AI 回答】\n{answer}",
        "tags": tags,
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/knowledge/ingest",
            json=payload,
            timeout=60,
        )
        if response.status_code == 200:
            result = response.json()
            return {"success": True, "doc_id": result.get("doc_id"), "stats": result.get("stats")}
        else:
            return {"success": False, "error": response.text}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "保存超时，请重试"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "无法连接到服务器"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def upload_document(file, poll_timeout: int = 120) -> Dict:
    """上传文档（支持轮询任务状态）"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{API_BASE_URL}/upload/document",
            files=files,
            timeout=60,
        )
        response.raise_for_status()
        result = response.json()

        # 轮询任务状态直到完成或超时
        task_id = result.get("task_id")
        if task_id:
            start_time = time.time()
            while time.time() - start_time < poll_timeout:
                time.sleep(1)
                try:
                    status_resp = requests.get(
                        f"{API_BASE_URL}/upload/tasks/{task_id}",
                        timeout=10,
                    )
                    if status_resp.status_code == 200:
                        status = status_resp.json()
                        if status.get("status") in ("completed", "failed"):
                            result["task_status"] = status
                            return result
                except Exception:
                    pass

            result["warning"] = "任务超时，但可能仍在后台处理"

        return result
    except Exception as e:
        return {"error": str(e)}


def get_documents() -> List[Dict]:
    """获取文档列表"""
    try:
        response = requests.get(f"{API_BASE_URL}/documents", timeout=10)
        if response.status_code == 200:
            return response.json().get("documents", [])
        return []
    except:
        return []


def get_stats() -> Dict:
    """获取统计信息"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}


def get_sessions() -> List[Dict]:
    """获取会话列表"""
    try:
        response = requests.get(f"{API_BASE_URL}/sessions", timeout=10)
        if response.status_code == 200:
            return response.json().get("sessions", [])
        return []
    except:
        return []


def load_session(session_id: str):
    """加载会话"""
    try:
        response = requests.get(f"{API_BASE_URL}/sessions/{session_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            st.session_state.session_id = session_id
            st.session_state.messages = [
                {"role": m["role"], "content": m["content"]}
                for m in data.get("messages", [])
            ]
            st.rerun()
    except Exception as e:
        st.error(f"加载会话失败: {e}")


def delete_session(session_id: str):
    """删除会话"""
    try:
        response = requests.delete(f"{API_BASE_URL}/sessions/{session_id}", timeout=10)
        if response.status_code == 200:
            if st.session_state.session_id == session_id:
                st.session_state.session_id = None
                st.session_state.messages = []
            st.rerun()
    except Exception as e:
        st.error(f"删除会话失败: {e}")


def clear_documents():
    """清空文档"""
    try:
        response = requests.delete(f"{API_BASE_URL}/documents", timeout=30)
        if response.status_code == 200:
            st.success("文档已清空")
            st.rerun()
    except Exception as e:
        st.error(f"清空失败: {e}")


def render_chat_tab():
    """渲染聊天标签页"""
    st.header("💬 智能问答")

    col1, col2 = st.columns([3, 1])
    with col1:
        use_kb = st.checkbox("🔍 使用知识库检索", value=True, help="从本地知识库检索相关文档")
    with col2:
        use_external = st.checkbox("🌐 允许公网大模型", value=True, help="知识库无结果时使用外部大模型")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("输入问题...", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            answer_source = ""
            try:
                for data in send_query_stream(prompt, use_kb, use_external):
                    if "error" in data:
                        message_placeholder.error(data["error"])
                        break
                    if data.get("done"):
                        answer_source = data.get("answer_source", "")
                        break
                    token = data.get("token", "")
                    full_response += token
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.session_state.pending_response = {"question": prompt, "answer": full_response}

                # 显示回答来源
                source_map = {
                    "knowledge_base": ("📚 知识库回答", "green"),
                    "external_llm": ("🌐 公网大模型回答", "blue"),
                    "none": ("⚠️ 无法回答", "red"),
                }
                src_label, src_color = source_map.get(answer_source, ("", ""))
                if src_label:
                    st.markdown(
                        f'<span style="color:{src_color}; font-size:0.85em;">{src_label}</span>',
                        unsafe_allow_html=True,
                    )

            except Exception as e:
                message_placeholder.error(f"请求失败: {e}")

    # 保存按钮放在 if prompt 块外面，确保按钮点击能被检测到
    pending = st.session_state.get("pending_response")
    if pending and pending.get("answer"):
        if st.button("💾 保存到知识库", key="save_kb_btn"):
            with st.spinner("正在保存..."):
                try:
                    save_data = {
                        "title": f"对话记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "content": f"【用户问题】\n{pending['question']}\n\n【AI 回答】\n{pending['answer']}",
                        "tags": ["对话记录", "AI回答"],
                    }
                    save_resp = requests.post(
                        f"{API_BASE_URL}/knowledge/ingest",
                        json=save_data,
                        timeout=60,
                    )
                    if save_resp.status_code == 200:
                        result = save_resp.json()
                        st.success(f"✅ 已保存到知识库 (doc_id: {result.get('doc_id', 'N/A')})")
                        st.session_state.pending_response = None
                    else:
                        st.error(f"保存失败: {save_resp.text}")
                except requests.exceptions.Timeout:
                    st.error("❌ 保存超时，请重试")
                except requests.exceptions.ConnectionError:
                    st.error("❌ 无法连接到服务器，请检查服务是否运行")
                except Exception as e:
                    st.error(f"❌ 保存失败: {str(e)}")

    with st.sidebar:
        st.subheader("📝 历史会话")

        sessions = get_sessions()
        if sessions:
            for session in sessions[:20]:
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(
                        f"🗂️ {session['title']}",
                        key=f"session_{session['id']}",
                        use_container_width=True,
                    ):
                        load_session(session["id"])
                with col2:
                    if st.button("🗑️", key=f"del_{session['id']}"):
                        delete_session(session["id"])
                        st.rerun()
        else:
            st.info("暂无历史会话")


def get_cleaned_documents() -> List[Dict]:
    """获取清洗后的文档列表"""
    try:
        response = requests.get(f"{API_BASE_URL}/documents/cleaned", timeout=10)
        if response.status_code == 200:
            return response.json().get("documents", [])
        return []
    except:
        return []


def get_cleaned_document(doc_id: str) -> Dict:
    """获取清洗后文档详情"""
    try:
        response = requests.get(f"{API_BASE_URL}/documents/cleaned/{doc_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def render_upload_tab():
    """渲染文档上传标签页"""
    st.header("📄 文档管理")

    tab1, tab2, tab3 = st.tabs(["上传文档", "文档列表", "清洗结果"])

    with tab1:
        st.subheader("上传新文档")

        uploaded_files = st.file_uploader(
            "选择文件",
            type=["pdf", "docx", "doc", "xlsx", "xls", "pptx", "ppt", "txt", "md", "json", "yaml", "yml", "html"],
            accept_multiple_files=True,
            help="支持 PDF、Word、Excel、PPT、TXT、Markdown、JSON、YAML、HTML 等格式",
        )

        if uploaded_files:
            st.write(f"已选择 {len(uploaded_files)} 个文件")

            for file in uploaded_files:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"📄 {file.name} ({file.size / 1024:.1f} KB)")
                with col2:
                    if st.button("上传", key=f"upload_{file.name}"):
                        with st.spinner(f"正在上传并处理 {file.name}..."):
                            result = upload_document(file)
                            if "error" in result:
                                st.error(result["error"])
                            elif result.get("task_status"):
                                status = result["task_status"]
                                if status.get("status") == "completed":
                                    st.success(f"✅ 上传成功！已生成 {status.get('success', 0)} 个文档块")
                                elif status.get("status") == "failed":
                                    st.error(f"❌ 处理失败: {status.get('error', '未知错误')}")
                                else:
                                    st.warning(f"⚠️ 任务状态: {status.get('status')}")
                            else:
                                st.info(result.get("message", "上传成功"))
                        time.sleep(1)
                        st.rerun()

        st.divider()

        st.subheader("📁 批量上传目录")

        dir_path = st.text_input(
            "目录路径",
            placeholder="例如: E:/文档",
            help="输入本地目录路径，系统将自动处理目录下的所有支持的文件",
        )

        col1, col2 = st.columns(2)
        with col1:
            recursive = st.checkbox("递归子目录", value=True)
        with col2:
            max_files = st.number_input("最大文件数", min_value=1, max_value=10000, value=100)

        if st.button("🚀 开始处理", type="primary") and dir_path:
            if Path(dir_path).exists() and Path(dir_path).is_dir():
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/upload/directory",
                        params={"directory_path": dir_path, "recursive": recursive, "max_files": max_files},
                        timeout=30,
                    )
                    if response.status_code == 200:
                        task_data = response.json()
                        task_id = task_data.get("task_id")
                        st.info(f"🚀 任务已启动，正在后台处理...")

                        # 轮询任务状态
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        while True:
                            time.sleep(2)
                            try:
                                status_resp = requests.get(
                                    f"{API_BASE_URL}/upload/tasks/{task_id}",
                                    timeout=10,
                                )
                                if status_resp.status_code == 200:
                                    status = status_resp.json()
                                    status_text.info(
                                        f"处理中... 已成功: {status.get('success', 0)}, "
                                        f"失败: {status.get('failed', 0)}, "
                                        f"总计: {status.get('total', 0)}"
                                    )
                                    if status.get("status") in ("completed", "failed"):
                                        result = status
                                        break
                            except Exception:
                                pass

                            if progress_bar.container:
                                current = result.get("success", 0) + result.get("failed", 0) if "result" in dir() else 0
                                total = result.get("total", max_files or 100)
                                progress_bar.progress(min(current / max(total, 1), 1.0))

                        progress_bar.empty()
                        status_text.empty()

                        if result.get("status") == "completed":
                            st.success(f"✅ 处理完成！成功: {result['success']}, 失败: {result['failed']}")
                            st.rerun()  # 自动刷新页面显示最新文档列表
                            with st.expander("查看详情"):
                                for r in result.get("results", []):
                                    if "error" in r:
                                        st.error(f"❌ {r.get('file', '未知')}: {r['error']}")
                                    else:
                                        st.success(f"✅ {r.get('title', '未知')}")
                        elif result.get("status") == "failed":
                            st.error(f"处理失败: {result.get('error', '未知错误')}")
                except Exception as e:
                    st.error(f"请求失败: {e}")
            else:
                st.error("目录不存在或路径无效")

    with tab2:
        st.subheader("已上传文档")

        docs = get_documents()
        if docs:
            stats = get_stats()
            if "documents" in stats:
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("文档总数", stats["documents"].get("total_documents", 0))
                with c2:
                    chunks = stats["documents"].get("total_chunks", 0)
                    st.metric("文档块总数", chunks)
                with c3:
                    indexed = stats["documents"].get("status_counts", {}).get("indexed", 0)
                    st.metric("已索引", indexed)

            st.divider()

            for doc in docs[:50]:
                with st.expander(f"📄 {doc.get('title', '未知文档')}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"类型: {doc.get('file_type', '未知')}")
                    with col2:
                        st.write(f"状态: {doc.get('status', '未知')}")
                    with col3:
                        st.write(f"块数: {doc.get('chunk_count', 0)}")
        else:
            st.info("暂无已上传的文档")

        if st.button("🗑️ 清空所有文档", type="secondary"):
            clear_documents()

    with tab3:
        st.subheader("清洗后文档")

        cleaned_docs = get_cleaned_documents()
        if cleaned_docs:
            st.write(f"共有 {len(cleaned_docs)} 个清洗后的文档")
            st.divider()

            for doc in cleaned_docs[:30]:
                with st.expander(f"📋 {doc.get('title', '未知标题')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"文档ID: `{doc.get('doc_id', '')[:8]}...`")
                        st.write(f"类型: {doc.get('doc_type', '未知')}")
                        st.write(f"状态: {doc.get('status', '未知')}")
                    with col2:
                        st.write(f"源文件: {Path(doc.get('source_file', '')).name}")
                        st.write(f"字符数: {doc.get('file_size', 0):,}")
                        st.write(f"清洗时间: {doc.get('created_at', '')[:19]}")

                    if st.button("🔍 查看详情", key=f"view_{doc.get('doc_id')}"):
                        detail = get_cleaned_document(doc.get('doc_id'))
                        if detail:
                            st.divider()
                            st.markdown("**清洗后的文本内容：**")
                            st.text_area(
                                "内容",
                                value=detail.get('content', '')[:5000],
                                height=300,
                                disabled=True,
                                label_visibility="collapsed"
                            )

                            if detail.get('metadata'):
                                st.divider()
                                st.markdown("**提取的元数据：**")
                                st.json(detail.get('metadata', {}))
                        else:
                            st.error("无法获取详情")
        else:
            st.info("暂无清洗后的文档。上传文档后即可查看清洗结果。")

            st.markdown("""
            **清洗流程说明：**

            1. **解析** - 从原始文件中提取纯文本
            2. **清洗** - 去除乱码、规范空白、检测文档类型
            3. **保存** - 清洗后的内容保存到 `data/cleaned/` 目录
            4. **分片** - 父子文档架构分割成块
            5. **向量化** - 使用 Embedding 模型转成向量
            6. **存储** - 保存到向量数据库
            """)


def render_settings_tab():
    """渲染设置标签页"""
    st.header("⚙️ 系统设置")

    st.subheader("API 连接状态")
    if check_api_connection():
        st.success("✅ API 服务已连接")

        stats = get_stats()
        if stats:
            st.json(stats)
    else:
        st.error("❌ API 服务未连接，请确保后端服务已启动")
        st.info("启动后端服务: python -m api.server")

    st.divider()

    st.subheader("模型配置")
    st.info("当前配置在 config/settings.py 中修改")

    st.code("""
# config/settings.py

# 本地 LLM (Ollama)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen3:8b"
OLLAMA_EMBED_MODEL = "bge-m3"

# 外部大模型 API
EXTERNAL_LLM_PROVIDER = "openai"  # openai/claude/dashscope/none
EXTERNAL_LLM_API_KEY = "your-api-key"
EXTERNAL_LLM_MODEL = "gpt-4o-mini"

# RAG 参数
TOP_K = 20              # 粗排召回数量
RERANK_TOP_K = 10       # 精排后返回数量
RERANK_THRESHOLD = 0.5  # 重排得分阈值
    """, language="python")

    st.divider()

    st.subheader("向量数据库")
    st.write(f"类型: {st.segmented_control('VECTOR_DB_TYPE', ['qdrant', 'chroma', 'file'], default='qdrant', disabled=True)}")
    st.write("如需更换数据库类型，请修改 config/settings.py")

    st.divider()

    st.subheader("关于")
    st.markdown("""
    **本地 RAG 知识库系统**

    功能特性：
    - 📄 支持多种文档格式（PDF、Word、Excel、PPT、TXT 等）
    - 🔍 父子文档分片，语义完整性保障
    - 🏆 向量检索 + Reranker 精排
    - 💬 上下文记忆，多轮对话
    - 🌐 支持外部大模型 API
    - 📚 文档管理与搜索
    """)


def main():
    init_session_state()

    st.markdown('<h1 class="main-header">📚 ALAN RAG 知识库</h1>', unsafe_allow_html=True)

    if not st.session_state.api_connected:
        st.session_state.api_connected = check_api_connection()

    if not st.session_state.api_connected:
        st.warning("⚠️ API 服务未连接，部分功能可能不可用")

    tab1, tab2, tab3 = st.tabs(["💬 问答", "📄 文档管理", "⚙️ 设置"])

    with tab1:
        render_chat_tab()
    with tab2:
        render_upload_tab()
    with tab3:
        render_settings_tab()


if __name__ == "__main__":
    main()
