#!/bin/bash
#===============================================================================
# 一键数据清洗脚本
# 用法: ./run_cleaning.sh [--workers N] [--resume]
#
# 要求:
#   1. 已挂载 NAS 到 /mnt/nas/raw (原始数据) 和 /mnt/nas/cleaned (清洗后)
#   2. 已安装 Python 依赖: pip install -r requirements.txt
#   3. 已配置 .env 文件（包含一体机地址）
#===============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录（脚本所在目录的父目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  NAS 数据清洗脚本${NC}"
echo -e "${BLUE}========================================${NC}"

# 默认参数
WORKERS=""
RESUME_FLAG=""
SCAN_ONLY=""
LOG_DIR="/mnt/nas/cleaned/logs"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --workers)
            WORKERS="--workers $2"
            shift 2
            ;;
        --resume)
            RESUME_FLAG="--resume"
            shift
            ;;
        --scan-only)
            SCAN_ONLY="--scan-only"
            shift
            ;;
        --help|-h)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --workers N     指定并发进程数（默认: CPU核心数-1）"
            echo "  --resume        启用断点续传（跳过已处理文件）"
            echo "  --scan-only     仅扫描并报告，不执行清洗"
            echo "  --help, -h      显示此帮助信息"
            exit 0
            ;;
        *)
            echo -e "${RED}未知参数: $1${NC}"
            exit 1
            ;;
    esac
done

# 激活虚拟环境
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    echo -e "${GREEN}激活虚拟环境...${NC}"
    source "$PROJECT_ROOT/venv/bin/activate"
elif [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
    echo -e "${GREEN}激活虚拟环境...${NC}"
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

# 创建日志目录
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/cleaning_$(date +%Y%m%d_%H%M%S).log"

# 检查 NAS 挂载
echo -e "${YELLOW}检查 NAS 挂载状态...${NC}"
if ! mountpoint -q /mnt/nas/raw 2>/dev/null; then
    echo -e "${RED}错误: /mnt/nas/raw 未挂载！${NC}"
    echo -e "${RED}请先挂载 NAS:${NC}"
    echo "  sudo mount -t nfs 192.168.x.x:/nas/raw /mnt/nas/raw"
    exit 1
fi

if ! mountpoint -q /mnt/nas/cleaned 2>/dev/null; then
    echo -e "${RED}错误: /mnt/nas/cleaned 未挂载！${NC}"
    echo -e "${RED}请先挂载 NAS:${NC}"
    echo "  sudo mount -t nfs 192.168.x.x:/nas/cleaned /mnt/nas/cleaned"
    exit 1
fi

echo -e "${GREEN}NAS 挂载检查通过${NC}"

# 检查源目录是否有文件
SOURCE_FILES=$(find /mnt/nas/raw -type f \( -name "*.pdf" -o -name "*.txt" -o -name "*.docx" -o -name "*.xlsx" \) 2>/dev/null | wc -l)
echo -e "源目录文件数: ${BLUE}${SOURCE_FILES}${NC}"

if [ "$SOURCE_FILES" -eq 0 ]; then
    echo -e "${YELLOW}警告: 源目录中没有找到待处理的文件${NC}"
    echo "将执行扫描模式..."
    SCAN_ONLY="--scan-only"
fi

# 打印配置
echo ""
echo -e "${BLUE}清洗配置:${NC}"
echo "  源目录:   /mnt/nas/raw"
echo "  目标目录: /mnt/nas/cleaned"
echo "  日志文件: $LOG_FILE"
[ -n "$WORKERS" ] && echo "  并发进程: $WORKERS"
[ -n "$RESUME_FLAG" ] && echo "  断点续传: 启用"
echo ""

# 确认执行
if [ -z "$SCAN_ONLY" ]; then
    read -p "确认开始清洗? (y/n): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "已取消"
        exit 0
    fi
fi

# 执行清洗
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}开始执行清洗任务...${NC}"
echo -e "${GREEN}========================================${NC}"

# 切换到项目目录
cd "$PROJECT_ROOT"

# 构建命令
CMD="python parsers/batch_processor.py \
    --source /mnt/nas/raw \
    --target /mnt/nas/cleaned \
    --db-path /mnt/nas/cleaned/.batch_progress.db \
    $WORKERS \
    --batch-size 20 \
    $RESUME_FLAG \
    $SCAN_ONLY"

echo "执行命令: $CMD"
echo ""

# 执行并记录日志
if [ -n "$SCAN_ONLY" ]; then
    # 扫描模式不记录到日志文件，直接输出
    eval $CMD
else
    # 执行模式同时输出到屏幕和日志文件
    $CMD 2>&1 | tee "$LOG_FILE"
fi

# 打印完成信息
echo ""
echo -e "${GREEN}========================================${NC}"
if [ -n "$SCAN_ONLY" ]; then
    echo -e "${GREEN}扫描完成！${NC}"
else
    echo -e "${GREEN}清洗任务完成！${NC}"
fi
echo -e "${GREEN}========================================${NC}"
echo "日志文件: $LOG_FILE"
echo "清洗后数据: /mnt/nas/cleaned"

# 显示统计信息
if [ -f "/mnt/nas/cleaned/.batch_progress.db" ]; then
    echo ""
    echo "处理统计:"
    python3 -c "
import sqlite3
conn = sqlite3.connect('/mnt/nas/cleaned/.batch_progress.db')
cur = conn.execute('SELECT status, COUNT(*) FROM processed_files GROUP BY status')
for row in cur:
    status_icon = '✓' if row[0] == 'success' else ('⊘' if row[0] == 'skipped' else '✗')
    print(f'  {status_icon} {row[0]}: {row[1]}')
conn.close()
" 2>/dev/null || true
fi

echo ""
echo -e "${BLUE}更多信息请查看: $LOG_FILE${NC}"
