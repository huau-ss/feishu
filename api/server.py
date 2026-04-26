"""
FastAPI 后端服务
提供 RAG 查询、文档上传、历史管理等 API
"""
import os
import logging
import tempfile
import uuid
import asyncio
from typing import List, Optional, Dict, Any
from pathlib import Path
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import uvicorn

from config import settings
from database import init_database
from core import get_rag_engine, get_history_manager, get_vector_store, get_document_storage
from llm import create_llm_client, ChatMessage
from feishu.webhook import router as feishu_router
from feishu.admin_router import router as admin_router
from api.personal_kb import router as personal_kb_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rag_engine = None
history_manager = None
_executor = ThreadPoolExecutor(max_workers=4)
_upload_tasks: Dict[str, Dict[str, Any]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_engine, history_manager

    init_database()

    logger.info("Initializing RAG Engine...")
    rag_engine = get_rag_engine()

    from config.settings import settings

    # 设置主 LLM（优先 OpenRouter，Hainan/Ollama 降级）
    if settings.EXTERNAL_LLM_API_KEY and settings.EXTERNAL_LLM_PROVIDER not in ("none", ""):
        llm_client = create_llm_client(
            provider=settings.EXTERNAL_LLM_PROVIDER,
            model=settings.EXTERNAL_LLM_MODEL,
            api_key=settings.EXTERNAL_LLM_API_KEY,
            base_url=settings.EXTERNAL_LLM_BASE_URL,
        )
        logger.info(f"Using OpenRouter LLM: {settings.EXTERNAL_LLM_MODEL} @ {settings.EXTERNAL_LLM_BASE_URL}")
    elif settings.HAINAN_LLM_BASE_URL:
        llm_client = create_llm_client(
            provider="openai",
            model=settings.HAINAN_LLM_MODEL,
            api_key=settings.HAINAN_LLM_API_KEY,
            base_url=settings.HAINAN_LLM_BASE_URL,
        )
        logger.info(f"Using Hainan AI LLM: {settings.HAINAN_LLM_MODEL} @ {settings.HAINAN_LLM_BASE_URL}")
    else:
        llm_client = create_llm_client(
            provider="ollama",
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
        )
        logger.info(f"Using Ollama LLM: {settings.OLLAMA_MODEL} @ {settings.OLLAMA_BASE_URL}")
    rag_engine.set_llm_client(llm_client)

    # 设置 external_llm_client（知识库无结果时的兜底 LLM）
    # 始终使用 OpenRouter 作为兜底（Hainan/Ollama 作为二级降级）
    if settings.EXTERNAL_LLM_API_KEY and settings.EXTERNAL_LLM_PROVIDER not in ("none", ""):
        # external_llm 也用 OpenRouter（因为 Hainan 已不可用）
        external_llm = create_llm_client(
            provider=settings.EXTERNAL_LLM_PROVIDER,
            model=settings.EXTERNAL_LLM_MODEL,
            api_key=settings.EXTERNAL_LLM_API_KEY,
            base_url=settings.EXTERNAL_LLM_BASE_URL,
        )
        logger.info(f"External LLM also using OpenRouter: {settings.EXTERNAL_LLM_MODEL}")
    elif settings.HAINAN_LLM_BASE_URL:
        external_llm = create_llm_client(
            provider="openai",
            model=settings.HAINAN_LLM_MODEL,
            api_key=settings.HAINAN_LLM_API_KEY,
            base_url=settings.HAINAN_LLM_BASE_URL,
        )
        logger.info(f"External LLM (Hainan): {settings.HAINAN_LLM_MODEL} @ {settings.HAINAN_LLM_BASE_URL}")
    else:
        external_llm = create_llm_client(
            provider="ollama",
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
        )
        logger.info(f"External LLM (Ollama): {settings.OLLAMA_MODEL} @ {settings.OLLAMA_BASE_URL}")

    rag_engine.set_external_llm_client(external_llm)

    history_manager = get_history_manager()

    from feishu.webhook import init_feishu_bot
    from feishu.bot import get_feishu_bot
    from feishu.employee_manager import get_skill_manager

    try:
        get_skill_manager()
        feishu_bot = get_feishu_bot(rag_engine=rag_engine)
        init_feishu_bot(feishu_bot)
        logger.info("Feishu Bot initialized successfully")
    except Exception as e:
        logger.warning(f"Feishu Bot initialization skipped: {e}")

    # 初始化 Obsidian 个人知识库表
    try:
        from core.personal_knowledge import init_obsidian_tables
        init_obsidian_tables()
        logger.info("Obsidian personal knowledge tables initialized")
    except Exception as e:
        logger.warning(f"Obsidian tables initialization skipped: {e}")

    logger.info("RAG Engine initialized successfully")

    yield

    logger.info("Shutting down...")


app = FastAPI(
    title="本地 RAG Demo API",
    description="本地 RAG 知识库问答系统",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feishu_router)
app.include_router(admin_router)
app.include_router(personal_kb_router)


class QueryRequest(BaseModel):
    question: str = Field(..., description="用户问题")
    session_id: Optional[str] = Field(None, description="会话 ID")
    use_knowledge_base: bool = Field(True, description="是否使用知识库")
    use_external_llm: bool = Field(True, description="知识库无结果时是否使用外部大模型")


class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []
    query: str
    from_knowledge_base: bool
    latency_ms: float
    model: str


class ChatMessageRequest(BaseModel):
    role: str
    content: str


class SessionCreateRequest(BaseModel):
    title: Optional[str] = None


class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: float
    updated_at: float


@app.get("/")
async def root():
    return {"message": "本地 RAG Demo API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "rag_engine": rag_engine is not None,
        "history_manager": history_manager is not None,
    }


@app.get("/stats")
async def get_stats():
    doc_storage = get_document_storage()
    vector_store = get_vector_store()

    return {
        "documents": doc_storage.get_stats(),
        "vectors": {"count": vector_store.count()},
        "sessions": history_manager.get_stats() if history_manager else {},
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    try:
        result = rag_engine.query(
            question=request.question,
            use_knowledge_base=request.use_knowledge_base,
            use_external_llm=request.use_external_llm,
            session_id=request.session_id,
        )

        if request.session_id and history_manager:
            history_manager.add_message(
                session_id=request.session_id,
                role="user",
                content=request.question,
            )
            history_manager.add_message(
                session_id=request.session_id,
                role="assistant",
                content=result.answer,
                metadata={"from_knowledge_base": result.from_knowledge_base},
            )

        return QueryResponse(
            answer=result.answer,
            sources=result.sources,
            query=result.query,
            from_knowledge_base=result.from_knowledge_base,
            latency_ms=result.latency_ms,
            model=result.model,
        )

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query/stream")
async def query_stream(request: QueryRequest):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    import asyncio
    import queue

    q: queue.Queue = queue.Queue()

    def run_stream():
        try:
            if request.session_id and history_manager:
                history_manager.add_message(
                    session_id=request.session_id,
                    role="user",
                    content=request.question,
                )

            full_response = []
            answer_source = ""
            token_count = 0
            for token, result in rag_engine.query_stream(
                question=request.question,
                use_knowledge_base=request.use_knowledge_base,
                use_external_llm=request.use_external_llm,
                session_id=request.session_id,
            ):
                full_response.append(token)
                answer_source = getattr(result, "answer_source", "")
                token_count += 1
                q.put(("token", token, False))

            if request.session_id and history_manager:
                history_manager.add_message(
                    session_id=request.session_id,
                    role="assistant",
                    content="".join(full_response),
                )

            logger.info(f"Stream complete: tokens={token_count}, source={answer_source}")
            q.put(("done", answer_source, True))
        except Exception as e:
            logger.error(f"Stream query failed: {e}")
            q.put(("error", str(e), True))

    async def generate():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, run_stream)

        while True:
            kind, data, done = await loop.run_in_executor(None, q.get)
            import json
            if kind == "error":
                yield f"data: {json.dumps({'error': data, 'done': True})}\n\n"
                break
            yield f"data: {json.dumps({'token': data if not done else '', 'done': done, 'answer_source': data if done else ''})}\n\n"
            if done:
                break

    return StreamingResponse(
        generate(),
        media_type="text/event-stream; charset=utf-8",
    )


@app.post("/upload/document")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )

    suffix = Path(file.filename).suffix.lower()
    allowed_exts = [
        '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
        '.txt', '.md', '.json', '.yaml', '.yml', '.html', '.htm',
        '.xml', '.zip', '.csv', '.rtf',
        '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm',
        '.mp3', '.wav', '.m4a', '.flac', '.ogg',
    ]
    if suffix not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}"
        )

    task_id = str(uuid.uuid4())
    _upload_tasks[task_id] = {
        "status": "running",
        "total": 1,
        "success": 0,
        "failed": 0,
        "error": None,
        "results": [],
    }

    def process():
        try:
            logger.info(f"Starting to process document: {file.filename}")
            result = rag_engine.process_document(tmp_path)
            _upload_tasks[task_id]["status"] = "completed"
            _upload_tasks[task_id]["success"] = 1
            _upload_tasks[task_id]["results"].append({
                "filename": file.filename,
                "status": "success",
                "result": result,
            })
            logger.info(f"Document processed successfully: {file.filename}, doc_id={result.get('doc_id')}")
        except Exception as e:
            logger.error(f"Background processing failed for {file.filename}: {e}", exc_info=True)
            _upload_tasks[task_id]["status"] = "failed"
            _upload_tasks[task_id]["failed"] = 1
            _upload_tasks[task_id]["error"] = str(e)
            _upload_tasks[task_id]["results"].append({
                "filename": file.filename,
                "status": "error",
                "error": str(e),
            })
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    background_tasks.add_task(process)

    return {
        "task_id": task_id,
        "message": "Document uploaded, processing in background",
        "filename": file.filename,
        "check_status": f"/upload/tasks/{task_id}",
    }


@app.post("/upload/documents")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    results = []
    for file in files:
        suffix = Path(file.filename).suffix.lower()
        if file.size and file.size > settings.MAX_FILE_SIZE:
            results.append({"filename": file.filename, "error": "File too large"})
            continue

        allowed_exts = [
            '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt',
            '.txt', '.md', '.json', '.yaml', '.yml', '.html', '.htm',
            '.xml', '.zip', '.csv', '.rtf',
            '.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm',
            '.mp3', '.wav', '.m4a', '.flac', '.ogg',
        ]
        if suffix not in allowed_exts:
            results.append({"filename": file.filename, "error": f"Unsupported file type: {suffix}"})
            continue

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        def process(path=tmp_path, name=file.filename):
            try:
                rag_engine.process_document(path)
            except Exception as e:
                logger.error(f"Processing failed for {name}: {e}")
            finally:
                Path(path).unlink(missing_ok=True)

        background_tasks.add_task(process)
        results.append({"filename": file.filename, "status": "processing"})

    return {"results": results}


class UploadTaskStatus(BaseModel):
    task_id: str
    status: str  # running / completed / failed
    total: int = 0
    success: int = 0
    failed: int = 0
    error: Optional[str] = None
    results: List[Dict[str, Any]] = []


@app.post("/upload/directory")
async def upload_directory(
    directory_path: str = Query(..., description="目录路径"),
    recursive: bool = Query(True, description="是否递归子目录"),
    max_files: Optional[int] = Query(None, description="最大文件数"),
):
    """异步上传目录，立即返回 task_id，UI 可轮询 /upload/tasks/{task_id}"""
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    path = Path(directory_path)
    if not path.exists() or not path.is_dir():
        raise HTTPException(status_code=400, detail="Invalid directory path")

    task_id = str(uuid.uuid4())
    _upload_tasks[task_id] = {
        "status": "running",
        "total": 0,
        "success": 0,
        "failed": 0,
        "error": None,
        "results": [],
    }

    def _do_upload():
        try:
            results = rag_engine.process_directory(
                directory=directory_path,
                recursive=recursive,
                max_files=max_files,
            )
            _upload_tasks[task_id].update({
                "status": "completed",
                "total": len(results),
                "success": sum(1 for r in results if "error" not in r),
                "failed": sum(1 for r in results if "error" in r),
                "results": results,
            })
        except Exception as e:
            _upload_tasks[task_id].update({
                "status": "failed",
                "error": str(e),
            })

    _executor.submit(_do_upload)

    return {"task_id": task_id, "status": "running", "message": "已开始处理"}


@app.get("/upload/tasks/{task_id}")
async def get_upload_task_status(task_id: str):
    """查询上传任务状态"""
    if task_id not in _upload_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return UploadTaskStatus(task_id=task_id, **_upload_tasks[task_id])


@app.get("/documents")
async def list_documents(status: Optional[str] = None):
    doc_storage = get_document_storage()
    docs = doc_storage.list_all(status=status)
    return {"documents": [vars(d) for d in docs]}


@app.post("/knowledge/ingest")
async def ingest_text(request: Request):
    """
    将文本直接灌入知识库（用于保存 LLM 回答等）
    
    请求体:
        - title: 文档标题
        - content: 要保存的内容
        - tags: 标签列表 (可选)
    """
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    body = await request.json()
    title = body.get("title", "未命名")
    content = body.get("content", "")
    tags = body.get("tags", [])

    if not content or not content.strip():
        raise HTTPException(status_code=400, detail="内容不能为空")

    logger.info(f"Ingesting text to knowledge base: title={title}, content_length={len(content)}, tags={tags}")

    import tempfile, os
    suffix = ".txt"
    
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="w", encoding="utf-8") as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        logger.info(f"Created temp file: {tmp_path}")
        
        doc_metadata = {"source": "llm_answer", "tags": tags, "original_title": title}
        logger.info(f"Calling process_document with metadata: {doc_metadata}")
        
        result = rag_engine.process_document(
            tmp_path,
            metadata=doc_metadata,
        )
        
        doc_id = result.get("doc_id")
        logger.info(f"Successfully ingested document: doc_id={doc_id}")
        
        return {
            "success": True,
            "doc_id": doc_id,
            "message": "已保存到知识库",
            "stats": {
                "parent_chunks": result.get("parent_chunks", 0),
                "child_chunks": result.get("child_chunks", 0),
                "total_chunks": result.get("total_chunks", 0),
            }
        }
    except Exception as e:
        logger.error(f"Failed to ingest text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")
    finally:
        if 'tmp_path' in locals():
            os.unlink(tmp_path)


@app.get("/documents/cleaned")
async def list_cleaned_documents():
    """列出所有清洗后的文档（不含内容）"""
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    documents = rag_engine.list_cleaned_documents()
    return {"documents": documents, "total": len(documents)}


@app.get("/documents/cleaned/{doc_id}")
async def get_cleaned_document(doc_id: str):
    """获取指定文档的清洗结果（Markdown 内容）"""
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    doc = rag_engine.get_cleaned_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Cleaned document not found")

    return {"content": doc}


@app.delete("/documents/cleaned/{doc_id}")
async def delete_cleaned_document(doc_id: str):
    """删除清洗后的文档文件"""
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    if rag_engine.delete_cleaned_document(doc_id):
        return {"message": "Cleaned document deleted"}
    raise HTTPException(status_code=404, detail="Cleaned document not found")


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    doc_storage = get_document_storage()
    doc = doc_storage.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    vector_store = get_vector_store()
    vector_store.delete([doc_id])

    doc_storage.delete(doc_id)

    return {"message": "Document deleted"}


@app.delete("/documents")
async def clear_documents():
    doc_storage = get_document_storage()
    vector_store = get_vector_store()

    doc_storage.clear_all()
    vector_store.clear()

    return {"message": "All documents cleared"}


@app.post("/sessions", response_model=SessionResponse)
async def create_session(request: SessionCreateRequest):
    if not history_manager:
        raise HTTPException(status_code=500, detail="History manager not initialized")

    session = history_manager.create_session(title=request.title)
    return SessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )


@app.get("/sessions")
async def list_sessions(limit: int = Query(50, le=100)):
    if not history_manager:
        raise HTTPException(status_code=500, detail="History manager not initialized")

    sessions = history_manager.list_sessions(limit=limit)
    return {
        "sessions": [
            {
                "id": s.id,
                "title": s.title,
                "created_at": s.created_at,
                "updated_at": s.updated_at,
                "message_count": len(s.messages),
            }
            for s in sessions
        ]
    }


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    if not history_manager:
        raise HTTPException(status_code=500, detail="History manager not initialized")

    session = history_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "id": session.id,
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp,
            }
            for m in session.messages
        ],
    }


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    if not history_manager:
        raise HTTPException(status_code=500, detail="History manager not initialized")

    if not history_manager.delete_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    return {"message": "Session deleted"}


@app.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: str,
    limit: Optional[int] = Query(None, le=100),
):
    if not history_manager:
        raise HTTPException(status_code=500, detail="History manager not initialized")

    messages = history_manager.get_messages(session_id, limit=limit)
    return {
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp,
            }
            for m in messages
        ]
    }


@app.get("/search")
async def search_documents(
    query: str = Query(..., description="搜索查询"),
    top_k: int = Query(10, le=50, description="返回数量"),
):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")

    results = rag_engine.retrieve(query, top_k=top_k)
    reranked = rag_engine.rerank_chunks(query, results)

    return {
        "query": query,
        "total": len(reranked),
        "results": [
            {
                "id": r.id,
                "content": r.content[:500],
                "score": r.score,
                "title": r.metadata.get("title", "未知"),
            }
            for r in reranked
        ],
    }


def run_server(host: str = None, port: int = None):
    uvicorn.run(
        "api.server:app",
        host=host or settings.API_HOST,
        port=port or settings.API_PORT,
        reload=False,
    )


if __name__ == "__main__":
    run_server()
