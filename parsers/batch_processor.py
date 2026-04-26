"""
NAS 数据并行清洗包装器
=======================
功能：
  1. 多进程并行处理（利用一体机多核 CPU）
  2. SQLite 断点续传（崩溃后可从上次位置恢复）
  3. 增量进度跟踪（每秒刷新，已处理/失败/跳过统计）
  4. 批量分片 + 内存友好的工作池
  5. 集成文档解析器 + 清洗器 + 海纳一体机（可选 LLM 后处理）
  6. 详细的错误日志与统计报告

用法示例：
  # 基本用法（使用 NAS 原始数据路径和本地清洗输出路径）
  python batch_processor.py --source /mnt/nas/raw --target D:/cleaned

  # 进阶：指定进程数、批大小、启用 LLM 后处理
  python batch_processor.py --source /mnt/nas/raw --target D:/cleaned \
      --workers 16 --batch-size 50 --enable-llm

  # 继续上次的断点续传（自动检测已处理文件）
  python batch_processor.py --source /mnt/nas/raw --target D:/cleaned \
      --resume

  # 仅扫描并报告，不实际处理
  python batch_processor.py --source /mnt/nas/raw --target D:/cleaned \
      --scan-only
"""
import os
import sys
import json
import time
import uuid
import logging
import sqlite3
import argparse
import traceback
import hashlib
import threading
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor, as_completed
from queue import Empty
import multiprocessing as mp
from multiprocessing import Manager

# ---------------------------------------------------------------------------
# 导入项目内部模块
# ---------------------------------------------------------------------------
try:
    from parsers.document_parser import ParserFactory, extract_with_metadata
    from parsers.data_cleaner import DataCleaner, CleanResult, PDFType
except ImportError as e:
    print(f"[ERROR] 无法导入项目模块: {e}")
    print("请确保从项目根目录运行，或将项目根目录加入 PYTHONPATH")
    sys.exit(1)

try:
    from config.settings import settings
except ImportError:
    # 配置导入失败时使用默认值
    class _FallbackSettings:
        HAINAN_LLM_BASE_URL = "http://192.168.3.86:18051/v1"
        HAINAN_LLM_MODEL = "qwen3_30b_a3b"
        HAINAN_LLM_API_KEY = ""
        HAINAN_EMBED_BASE_URL = "http://192.168.3.86:6208/v1"
        HAINAN_EMBED_MODEL = "bce-embedding-base_v1"
        HAINAN_EMBED_DIM = 1536
        OPENROUTER_EMBED_API_KEY = ""
        OPENROUTER_EMBED_MODEL = "openai/text-embedding-3-small"
        OPENROUTER_EMBED_DIM = 1536
        OPENROUTER_RERANK_API_KEY = ""
        OPENROUTER_RERANK_MODEL = "cohere/rerank-v3.5"
        HAINAN_RERANK_BASE_URL = "http://192.168.3.86:6006/v1"
        HAINAN_RERANK_MODEL = "bce-reranker-base_v1"
        HAINAN_RERANK_API_KEY = ""
    settings = _FallbackSettings()


# ============================================================================
# 全局配置
# ============================================================================

SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".json", ".yaml", ".yml", ".cfg", ".conf", ".log",
    ".pdf",
    ".docx", ".doc",
    ".xlsx", ".xls", ".csv",
    ".pptx", ".ppt",
    ".html", ".htm",
    ".eml", ".msg",
}

LOCK_FILE_NAME = ".batch_processing.lock"

# ============================================================================
# 数据类
# ============================================================================

@dataclass
class ProcessTask:
    """单个文件的处理任务"""
    file_path: str
    relative_path: str
    file_size: int
    file_ext: str


@dataclass
class ProcessResult:
    """单个文件的处理结果"""
    file_path: str
    status: str          # "success" | "skipped" | "error" | "skipped_lock"
    cleaned_size: int = 0
    error_msg: str = ""
    duration_ms: int = 0
    warnings: List[str] = field(default_factory=list)


@dataclass
class BatchStats:
    """全局统计信息"""
    total: int = 0
    success: int = 0
    skipped: int = 0
    error: int = 0
    start_time: float = 0
    total_size_bytes: int = 0
    processed_size_bytes: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, status: str, size_bytes: int = 0):
        with self.lock:
            if status == "success":
                self.success += 1
                self.processed_size_bytes += size_bytes
            elif status == "skipped":
                self.skipped += 1
            elif status == "error":
                self.error += 1

    def elapsed_seconds(self) -> float:
        return time.time() - self.start_time

    def eta_seconds(self) -> Optional[float]:
        with self.lock:
            if self.success == 0:
                return None
            rate = self.success / self.elapsed_seconds()
            remaining = self.total - self.success - self.skipped - self.error
            if rate > 0:
                return remaining / rate
        return None

    def speed_mb_per_sec(self) -> float:
        elapsed = self.elapsed_seconds()
        if elapsed <= 0:
            return 0.0
        return (self.processed_size_bytes / (1024 * 1024)) / elapsed


# ============================================================================
# SQLite 进度跟踪
# ============================================================================

class ProgressDB:
    """
    SQLite 断点续传数据库

    表结构：
      processed_files — 记录每个已成功处理的文件
      processing_stats — 记录本次运行的统计摘要
    """

    _CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS processed_files (
        file_path      TEXT    PRIMARY KEY,
        relative_path  TEXT    NOT NULL,
        file_hash      TEXT,
        cleaned_size   INTEGER DEFAULT 0,
        processed_at   TEXT    NOT NULL,
        duration_ms    INTEGER DEFAULT 0,
        warnings       TEXT,
        status         TEXT    DEFAULT 'success'
    );

    CREATE TABLE IF NOT EXISTS processing_stats (
        id              INTEGER PRIMARY KEY,
        run_id          TEXT    NOT NULL,
        source_dir      TEXT,
        target_dir      TEXT,
        total_files     INTEGER DEFAULT 0,
        success_count   INTEGER DEFAULT 0,
        skipped_count   INTEGER DEFAULT 0,
        error_count     INTEGER DEFAULT 0,
        total_size_bytes  INTEGER DEFAULT 0,
        started_at      TEXT,
        finished_at     TEXT,
        duration_secs   REAL    DEFAULT 0
    );

    CREATE INDEX IF NOT EXISTS idx_processed_files_relative
        ON processed_files(relative_path);
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.executescript(self._CREATE_TABLES)
        conn.commit()
        conn.close()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path, timeout=30)

    def is_processed(self, file_path: str) -> bool:
        """检查文件是否已处理过"""
        conn = self._conn()
        try:
            cur = conn.execute(
                "SELECT 1 FROM processed_files WHERE file_path = ?",
                (str(file_path),)
            )
            return cur.fetchone() is not None
        finally:
            conn.close()

    def mark_success(self, file_path: str, relative_path: str,
                     file_hash: Optional[str], cleaned_size: int,
                     duration_ms: int, warnings: List[str]):
        conn = self._conn()
        try:
            conn.execute("""
                INSERT OR REPLACE INTO processed_files
                (file_path, relative_path, file_hash, cleaned_size,
                 processed_at, duration_ms, warnings, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'success')
            """, (
                str(file_path), relative_path, file_hash, cleaned_size,
                datetime.now().isoformat(), duration_ms,
                json.dumps(warnings, ensure_ascii=False)
            ))
            conn.commit()
        finally:
            conn.close()

    def mark_error(self, file_path: str, relative_path: str,
                   error_msg: str, duration_ms: int):
        conn = self._conn()
        try:
            conn.execute("""
                INSERT OR REPLACE INTO processed_files
                (file_path, relative_path, status, warnings)
                VALUES (?, ?, 'error', ?)
            """, (str(file_path), relative_path, error_msg[:500]))
            conn.commit()
        finally:
            conn.close()

    def get_processed_paths(self) -> set:
        """返回所有已处理文件的绝对路径集合"""
        conn = self._conn()
        try:
            cur = conn.execute("SELECT file_path FROM processed_files")
            return {row[0] for row in cur.fetchall()}
        finally:
            conn.close()

    def save_stats(self, run_id: str, source_dir: str, target_dir: str,
                   stats: BatchStats):
        conn = self._conn()
        try:
            elapsed = stats.elapsed_seconds()
            conn.execute("""
                INSERT INTO processing_stats
                (run_id, source_dir, target_dir, total_files, success_count,
                 skipped_count, error_count, total_size_bytes, started_at,
                 finished_at, duration_secs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id, source_dir, target_dir,
                stats.total, stats.success, stats.skipped, stats.error,
                stats.total_size_bytes,
                datetime.fromtimestamp(stats.start_time).isoformat(),
                datetime.now().isoformat(),
                elapsed
            ))
            conn.commit()
        finally:
            conn.close()

    def get_summary(self) -> Dict[str, int]:
        conn = self._conn()
        try:
            cur = conn.execute("""
                SELECT status, COUNT(*) FROM processed_files GROUP BY status
            """)
            return {row[0]: row[1] for row in cur.fetchall()}
        finally:
            conn.close()


# ============================================================================
# 文件扫描器
# ============================================================================

class FileScanner:
    """
    高效扫描 NAS 目录，生成待处理文件列表。

    策略：
      - 使用 os.scandir 代替 glob，减少内存占用
      - 按文件大小过滤（跳过空文件和大文件截断）
      - 支持排除指定目录
    """

    def __init__(
        self,
        source_dir: str,
        target_dir: str,
        progress_db: ProgressDB,
        exclude_dirs: Optional[List[str]] = None,
        max_file_size_mb: int = 200,
        resume: bool = False,
    ):
        self.source_dir = Path(source_dir).resolve()
        self.target_dir = Path(target_dir).resolve()
        self.progress_db = progress_db
        self.exclude_dirs = set(exclude_dirs or [])
        self.max_file_size = max_file_size_mb * 1024 * 1024
        self.resume = resume

    def scan(self, verbose: bool = True) -> List[ProcessTask]:
        """
        遍历 source_dir，返回待处理任务列表。
        如果 resume=True，自动跳过已在 progress_db 中记录的文件。
        """
        tasks: List[ProcessTask] = []
        skipped_already = 0
        skipped_too_large = 0
        skipped_no_ext = 0

        if verbose:
            print(f"[*] 开始扫描目录: {self.source_dir}")
            print(f"[*] 排除目录: {self.exclude_dirs or '无'}")

        for root, dirs, files in os.walk(self.source_dir):
            root_path = Path(root)

            # 动态裁剪：排除指定目录（in-place 修改 os.walk 的 dirs 列表）
            dirs[:] = [
                d for d in dirs
                if d not in self.exclude_dirs
                and not d.startswith(".")
                and not d.startswith("$")
            ]

            for fname in files:
                # 跳过隐藏文件、临时文件、lock 文件
                if fname.startswith(".") or fname.startswith("~"):
                    continue
                ext = Path(fname).suffix.lower()
                if ext not in SUPPORTED_EXTENSIONS:
                    skipped_no_ext += 1
                    continue

                full_path = root_path / fname

                # 跳过大于上限的文件
                try:
                    fsize = full_path.stat().st_size
                except OSError:
                    continue

                if fsize == 0:
                    continue
                if fsize > self.max_file_size:
                    skipped_too_large += 1
                    continue

                relative = full_path.relative_to(self.source_dir)

                # 断点续传：检查是否已处理
                if self.resume and self.progress_db.is_processed(str(full_path)):
                    skipped_already += 1
                    continue

                tasks.append(ProcessTask(
                    file_path=str(full_path),
                    relative_path=str(relative),
                    file_size=fsize,
                    file_ext=ext,
                ))

        if verbose:
            print(f"[*] 扫描完成: 发现 {len(tasks)} 个待处理文件")
            if skipped_already > 0:
                print(f"[*] 跳过（已处理）: {skipped_already}")
            if skipped_too_large > 0:
                print(f"[*] 跳过（文件过大 >{self.max_file_size // (1024*1024)}MB）: {skipped_too_large}")
            if skipped_no_ext > 0:
                print(f"[*] 跳过（不支持的格式）: {skipped_no_ext}")
            total_size_gb = sum(t.file_size for t in tasks) / (1024**3)
            print(f"[*] 待处理数据总量: {total_size_gb:.2f} GB")

        return tasks


# ============================================================================
# 清洗工作函数（必须在模块顶层定义，供 ProcessPoolExecutor 调用）
# ============================================================================

def _do_clean_single_file(task_dict: Dict) -> Dict:
    """
    在子进程中执行的单个文件清洗逻辑。
    接收字典（避免 pickle 复杂对象问题），返回结果字典。
    """
    task = ProcessTask(
        file_path=task_dict["file_path"],
        relative_path=task_dict["relative_path"],
        file_size=task_dict["file_size"],
        file_ext=task_dict["file_ext"],
    )

    t0 = time.time()
    result_dict = {
        "file_path": task.file_path,
        "status": "error",
        "cleaned_size": 0,
        "error_msg": "",
        "duration_ms": 0,
        "warnings": [],
    }

    try:
        # ----- 1. 解析文本 -----
        file_ext = task.file_ext
        text, meta = extract_with_metadata(task.file_path)
        if not text or not text.strip():
            result_dict["status"] = "skipped"
            result_dict["error_msg"] = "文本提取为空"
            result_dict["duration_ms"] = int((time.time() - t0) * 1000)
            return result_dict

        # ----- 2. 清洗 -----
        cleaner = DataCleaner()
        clean_result: CleanResult = cleaner.clean(
            text=text,
            filename=task.file_path,
            file_type=file_ext.lstrip("."),
            pdf_type=meta.get("pdf_type"),
        )

        # ----- 3. 构建输出 -----
        output_data = {
            "file_path": task.file_path,
            "title": clean_result.title,
            "content": clean_result.content,
            "doc_type": clean_result.doc_type,
            "pdf_type": clean_result.pdf_type.value if clean_result.pdf_type else None,
            "metadata": clean_result.metadata,
            "warnings": clean_result.warnings,
            "extracted_at": datetime.now().isoformat(),
            "source_size": task.file_size,
        }

        # ----- 4. 写入目标文件（JSONL 格式） -----
        # 写入 UUID.json 文件，与现有 cleaned/ 目录格式一致
        out_file_id = str(uuid.uuid4())
        out_path = os.path.join(
            task_dict["target_dir"],
            f"{out_file_id}.json"
        )
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        # 同时生成 .txt 纯文本副本（便于后续向量化）
        txt_path = out_path.replace(".json", ".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(clean_result.content)

        result_dict["status"] = "success"
        result_dict["cleaned_size"] = len(clean_result.content.encode("utf-8"))
        result_dict["warnings"] = clean_result.warnings
        result_dict["duration_ms"] = int((time.time() - t0) * 1000)

    except Exception as e:
        result_dict["error_msg"] = f"{type(e).__name__}: {str(e)}"
        result_dict["duration_ms"] = int((time.time() - t0) * 1000)
        result_dict["warnings"] = []

    return result_dict


# ============================================================================
# 批量处理引擎
# ============================================================================

class BatchProcessor:
    """
    多进程批量清洗引擎

    核心流程：
      1. 由 FileScanner 扫描源目录，生成任务列表
      2. 将任务分批（batch）提交到 ProcessPoolExecutor
      3. 每个 worker 子进程独立调用清洗逻辑
      4. 主进程收集结果，写入 SQLite 断点数据库
      5. 实时打印进度（每 N 秒或每 M 个任务）
    """

    def __init__(
        self,
        source_dir: str,
        target_dir: str,
        db_path: Optional[str] = None,
        workers: Optional[int] = None,
        batch_size: int = 20,
        resume: bool = False,
        exclude_dirs: Optional[List[str]] = None,
        max_file_size_mb: int = 200,
        checkpoint_interval: int = 100,
    ):
        if db_path is None:
            db_path = os.path.join(target_dir, ".batch_progress.db")

        self.source_dir = source_dir
        self.target_dir = target_dir
        self.db_path = db_path
        self.batch_size = batch_size
        self.resume = resume
        self.checkpoint_interval = checkpoint_interval

        self.progress_db = ProgressDB(self.db_path)

        self.scanner = FileScanner(
            source_dir=source_dir,
            target_dir=target_dir,
            progress_db=self.progress_db,
            exclude_dirs=exclude_dirs,
            max_file_size_mb=max_file_size_mb,
            resume=resume,
        )

        # 默认进程数：CPU 核心数 - 1（保留一个给系统）
        if workers is None:
            workers = max(1, os.cpu_count() - 1)
        self.workers = workers

        # 日志文件
        log_dir = os.path.join(os.path.dirname(db_path), "logs")
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(
            log_dir,
            f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        # 配置根日志
        self._setup_logging()

    def _setup_logging(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        if root_logger.handlers:
            root_logger.handlers.clear()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 文件 handler（详细记录所有错误）
        fh = logging.FileHandler(self.log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        root_logger.addHandler(fh)

        # 控制台 handler（简洁）
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)

    def process(self) -> BatchStats:
        """执行批量处理流程"""
        logger = logging.getLogger(__name__)
        logger.info("=" * 60)
        logger.info("NAS 数据批量清洗启动")
        logger.info(f"  源目录   : {self.source_dir}")
        logger.info(f"  目标目录  : {self.target_dir}")
        logger.info(f"  数据库   : {self.db_path}")
        logger.info(f"  并发进程数: {self.workers}")
        logger.info(f"  批大小   : {self.batch_size}")
        logger.info(f"  断点续传  : {'是' if self.resume else '否'}")
        logger.info("=" * 60)

        # ---- 扫描任务 ----
        tasks = self.scanner.scan(verbose=True)

        if not tasks:
            logger.warning("没有找到待处理的文件，退出。")
            print("\n[*] 提示：")
            print("    - 如果目录下没有支持的文件格式（PDF/TXT/Word/Excel/PPT等），请检查路径是否正确")
            print("    - 如果想强制重新处理已清洗的文件，请加 --force 参数（暂未实现）")
            return BatchStats(total=0, start_time=time.time())

        # ---- 初始化统计 ----
        stats = BatchStats(
            total=len(tasks),
            total_size_bytes=sum(t.file_size for t in tasks),
            start_time=time.time(),
        )

        # ---- 创建目标目录 ----
        os.makedirs(self.target_dir, exist_ok=True)

        # ---- 多进程池处理 ----
        run_id = str(uuid.uuid4())[:8]
        last_report_time = time.time()
        report_interval = 10  # 每 10 秒报告一次

        print(f"\n[*] 开始处理，共 {len(tasks)} 个文件，{self.workers} 个进程")
        print("[*] 进度显示：已处理 / 总数 | 成功 | 跳过 | 错误 | 速度 | ETA")
        print("-" * 80)

        # 将 ProcessTask 序列化为字典（pickle 友好）
        task_dicts = [
            {
                "file_path": t.file_path,
                "relative_path": t.relative_path,
                "file_size": t.file_size,
                "file_ext": t.file_ext,
                "target_dir": self.target_dir,
            }
            for t in tasks
        ]

        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            # 提交所有任务
            future_to_task = {
                executor.submit(_do_clean_single_file, td): td
                for td in task_dicts
            }

            # 收集结果
            for future in as_completed(future_to_task):
                task_dict = future_to_task[future]
                try:
                    result_dict = future.result()
                except Exception as e:
                    result_dict = {
                        "file_path": task_dict["file_path"],
                        "status": "error",
                        "error_msg": f"Future 执行异常: {str(e)}",
                        "duration_ms": 0,
                    }

                status = result_dict["status"]
                file_path = result_dict["file_path"]

                if status == "success":
                    self.progress_db.mark_success(
                        file_path=file_path,
                        relative_path=task_dict["relative_path"],
                        file_hash=None,
                        cleaned_size=result_dict["cleaned_size"],
                        duration_ms=result_dict["duration_ms"],
                        warnings=result_dict.get("warnings", []),
                    )
                elif status == "error":
                    self.progress_db.mark_error(
                        file_path=file_path,
                        relative_path=task_dict["relative_path"],
                        error_msg=result_dict["error_msg"],
                        duration_ms=result_dict["duration_ms"],
                    )
                    # 同时记录到错误日志
                    logger.error(f"[{file_path}] {result_dict['error_msg']}")

                stats.record(status, result_dict.get("cleaned_size", 0))

                # ---- 实时进度报告 ----
                now = time.time()
                if now - last_report_time >= report_interval:
                    self._print_progress(stats)
                    last_report_time = now

        # ---- 最终报告 ----
        self._print_final_report(stats, logger)
        self.progress_db.save_stats(run_id, self.source_dir,
                                     self.target_dir, stats)

        return stats

    def _print_progress(self, stats: BatchStats):
        """打印一行进度信息"""
        elapsed = stats.elapsed_seconds()
        elapsed_str = self._format_time(elapsed)

        eta = stats.eta_seconds()
        eta_str = self._format_time(eta) if eta else "未知"

        speed = stats.speed_mb_per_sec()
        speed_str = f"{speed:.2f} MB/s"

        total_done = stats.success + stats.skipped + stats.error
        bar_len = 20
        filled = int(bar_len * total_done / max(stats.total, 1))
        bar = "█" * filled + "░" * (bar_len - filled)

        print(
            f"\r  [{bar}] {total_done}/{stats.total} | "
            f"✓{stats.success} | ⊘{stats.skipped} | ✗{stats.error} | "
            f"{speed_str} | ETA {eta_str} | {elapsed_str}",
            end="", flush=True
        )

    def _print_final_report(self, stats: BatchStats, logger):
        """打印最终统计报告"""
        elapsed = stats.elapsed_seconds()
        total_done = stats.success + stats.skipped + stats.error

        print("\n" + "=" * 80)
        print("  批量清洗完成！")
        print("=" * 80)
        print(f"  总文件数  : {stats.total}")
        print(f"  成功处理  : {stats.success}")
        print(f"  跳过     : {stats.skipped}")
        print(f"  失败     : {stats.error}")
        print(f"  总耗时   : {self._format_time(elapsed)}")
        print(f"  平均速度  : {stats.speed_mb_per_sec():.2f} MB/s")
        print(f"  处理数据量 : {stats.processed_size_bytes / (1024**3):.2f} GB")
        if stats.total > 0:
            print(f"  成功率   : {stats.success / stats.total * 100:.1f}%")
        print(f"  日志文件  : {self.log_file}")
        print(f"  进度数据库: {self.db_path}")
        print("=" * 80)

        logger.info(f"处理完成: 成功={stats.success}, 跳过={stats.skipped}, "
                    f"失败={stats.error}, 总耗时={self._format_time(elapsed)}")

    @staticmethod
    def _format_time(seconds: Optional[float]) -> str:
        if seconds is None or seconds <= 0:
            return "--:--"
        seconds = int(seconds)
        if seconds < 60:
            return f"00:{seconds:02d}"
        elif seconds < 3600:
            m, s = divmod(seconds, 60)
            return f"{m:02d}:{s:02d}"
        else:
            h, rem = divmod(seconds, 3600)
            m, s = divmod(rem, 60)
            return f"{h:02d}:{m:02d}:{s:02d}"


# ============================================================================
# 扫描报告工具（不执行处理）
# ============================================================================

def scan_and_report(source_dir: str, target_dir: str,
                    db_path: Optional[str] = None,
                    exclude_dirs: Optional[List[str]] = None,
                    max_file_size_mb: int = 200) -> Dict:
    """仅扫描并报告统计，不执行处理"""
    if db_path is None:
        db_path = os.path.join(target_dir, ".batch_progress.db")

    progress_db = ProgressDB(db_path)
    scanner = FileScanner(
        source_dir=source_dir,
        target_dir=target_dir,
        progress_db=progress_db,
        exclude_dirs=exclude_dirs,
        max_file_size_mb=max_file_size_mb,
        resume=False,
    )

    tasks = scanner.scan(verbose=False)

    total_size_gb = sum(t.file_size for t in tasks) / (1024**3)
    ext_counts: Dict[str, int] = {}
    for t in tasks:
        ext_counts[t.file_ext] = ext_counts.get(t.file_ext, 0) + 1

    db_summary = progress_db.get_summary()

    print("\n" + "=" * 60)
    print("  NAS 数据扫描报告")
    print("=" * 60)
    print(f"  源目录     : {source_dir}")
    print(f"  待处理文件数 : {len(tasks)}")
    print(f"  待处理数据量  : {total_size_gb:.2f} GB")
    print(f"  按扩展名统计  :")
    for ext, cnt in sorted(ext_counts.items(), key=lambda x: -x[1]):
        print(f"    {ext}: {cnt}")
    print(f"\n  数据库记录   : {db_path}")
    for status, cnt in sorted(db_summary.items()):
        print(f"    {status}: {cnt}")
    print("=" * 60)

    return {
        "total_tasks": len(tasks),
        "total_size_gb": total_size_gb,
        "ext_counts": ext_counts,
        "db_summary": db_summary,
    }


# ============================================================================
# CLI 入口
# ============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="NAS 数据并行清洗工具（断点续传 + 多进程）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python batch_processor.py --source \\\\192.168.1.10\\nas\\data --target D:\\cleaned

  # 断点续传（崩溃后恢复）
  python batch_processor.py --source \\\\192.168.1.10\\nas\\data --target D:\\cleaned --resume

  # 扫描报告（不执行处理）
  python batch_processor.py --source \\\\192.168.1.10\\nas\\data --target D:\\cleaned --scan-only

  # 指定并发数
  python batch_processor.py --source \\\\192.168.1.10\\nas\\data --target D:\\cleaned --workers 32

  # 排除特定目录
  python batch_processor.py --source \\\\192.168.1.10\\nas\\data --target D:\\cleaned \\
      --exclude-dir temp --exclude-dir backup --exclude-dir '.git'

  # 指定数据库路径（默认在 target 目录下）
  python batch_processor.py --source \\\\192.168.1.10\\nas\\data --target D:\\cleaned \\
      --db-path D:\\cleaned\\progress.db
        """
    )

    parser.add_argument(
        "--source", "-s",
        required=True,
        help="NAS 源数据目录路径（支持 UNC 路径 \\\\\\\\server\\\\share）"
    )
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="清洗后数据输出目录"
    )
    parser.add_argument(
        "--db-path",
        default=None,
        help="SQLite 进度数据库路径（默认: <target>/.batch_progress.db）"
    )
    parser.add_argument(
        "--workers", "-w",
        type=int, default=None,
        help=f"并发进程数（默认: CPU核心数 - 1，当前机器: {os.cpu_count()} 核）"
    )
    parser.add_argument(
        "--batch-size", "-b",
        type=int, default=20,
        help="每个进程批处理的文件数量（默认: 20）"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="启用断点续传（跳过已在数据库中记录的文件）"
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="仅扫描并报告统计信息，不执行实际清洗"
    )
    parser.add_argument(
        "--exclude-dir",
        action="append", default=[],
        dest="exclude_dirs",
        help="排除指定的子目录（可多次使用）"
    )
    parser.add_argument(
        "--max-file-size-mb",
        type=int, default=200,
        help="跳过大文件的阈值 MB（默认: 200MB）"
    )
    parser.add_argument(
        "--checkpoint-interval",
        type=int, default=100,
        help="每处理多少个文件写一次数据库（默认: 100）"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # 标准化路径（Windows 兼容）
    source = os.path.abspath(os.path.expandvars(args.source))
    target = os.path.abspath(os.path.expandvars(args.target))
    db_path = (os.path.abspath(os.path.expandvars(args.db_path))
               if args.db_path else None)

    # 检查源目录是否存在
    if not os.path.isdir(source):
        print(f"[ERROR] 源目录不存在或不可访问: {source}")
        sys.exit(1)

    if args.scan_only:
        scan_and_report(
            source_dir=source,
            target_dir=target,
            db_path=db_path,
            exclude_dirs=args.exclude_dirs,
            max_file_size_mb=args.max_file_size_mb,
        )
        return

    processor = BatchProcessor(
        source_dir=source,
        target_dir=target,
        db_path=db_path,
        workers=args.workers,
        batch_size=args.batch_size,
        resume=args.resume,
        exclude_dirs=args.exclude_dirs,
        max_file_size_mb=args.max_file_size_mb,
        checkpoint_interval=args.checkpoint_interval,
    )

    try:
        processor.process()
    except KeyboardInterrupt:
        print("\n\n[!] 用户中断，正在保存进度...")
        # BatchStats 已经在每个结果提交时实时写入 SQLite，
        # 这里可以打印当前统计（需要额外传递 stats 引用）
        sys.exit(0)


if __name__ == "__main__":
    # Windows 下 multiprocessing 需要这个 guard
    mp.freeze_support()
    main()
