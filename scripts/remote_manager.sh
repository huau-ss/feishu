#!/bin/bash
#===============================================================================
# 远程服务器任务管理脚本
# 用于从本机管理虚拟机上的清洗任务
#
# 用法:
#   ./remote_manager.sh status      - 查看当前任务状态
#   ./remote_manager.sh start       - 启动清洗任务
#   ./remote_manager.sh stop        - 停止当前任务
#   ./remote_manager.sh logs [n]    - 查看日志（默认最后100行）
#   ./remote_manager.sh progress    - 查看清洗进度
#   ./remote_manager.sh ssh         - 打开 SSH 连接
#   ./remote_manager.sh setup      - 在服务器上初始化环境
#===============================================================================

# ==================== 配置区域（请根据实际情况修改） ====================

# 虚拟机/服务器配置
SERVER_HOST="192.168.3.100"          # 服务器IP（请修改）
SERVER_USER="your_username"           # 服务器用户名（请修改）
SERVER_PORT="22"                     # SSH端口（默认22）

# 服务器上的项目路径
REMOTE_PROJECT_DIR="/opt/rag-cleaner"

# NAS 配置
NAS_RAW_PATH="/mnt/nas/raw"          # 原始数据路径
NAS_CLEANED_PATH="/mnt/nas/cleaned"  # 清洗后数据路径

# 一体机配置（服务器上需要能访问）
# HAINAN_LLM_BASE_URL="http://192.168.3.86:18051/v1"

# 清洗参数
CLEANING_WORKERS=""                   # 留空使用默认（CPU核心数-1），或指定如 "8"
CLEANING_BATCH_SIZE="20"

# ==================== 以下内容通常不需要修改 ====================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 脚本自身路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# SSH 命令
SSH_CMD="ssh -p ${SERVER_PORT} ${SERVER_USER}@${SERVER_HOST}"
SCP_CMD="scp -P ${SERVER_PORT}"

#===============================================================================
# 辅助函数
#===============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

#===============================================================================
# SSH 执行远程命令
#===============================================================================

remote_exec() {
    $SSH_CMD "$1"
}

remote_exec_sudo() {
    $SSH_CMD "sudo $1"
}

#===============================================================================
# 同步文件到服务器
#===============================================================================

sync_to_server() {
    log_info "同步本地文件到服务器..."

    # 排除不需要同步的目录
    EXCLUDE_OPTS="--exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' --exclude='.venv' --exclude='node_modules'"

    rsync -avz -e "ssh -p ${SERVER_PORT}" \
        $EXCLUDE_OPTS \
        "${SCRIPT_DIR}/../" \
        "${SERVER_USER}@${SERVER_HOST}:${REMOTE_PROJECT_DIR}/"

    log_success "文件同步完成"
}

#===============================================================================
# 初始化服务器环境
#===============================================================================

cmd_setup() {
    log_info "初始化服务器环境..."

    # 创建目录结构
    remote_exec "mkdir -p ${REMOTE_PROJECT_DIR}
mkdir -p /mnt/nas/raw
mkdir -p /mnt/nas/cleaned"

    # 同步代码
    sync_to_server

    # 安装依赖
    log_info "安装 Python 依赖..."
    remote_exec "cd ${REMOTE_PROJECT_DIR}
if [ ! -d 'venv' ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pymupdf python-docx openpyxl python-pptx"

    # 创建 .env 文件
    log_info "创建配置文件..."
    remote_exec "cat > ${REMOTE_PROJECT_DIR}/.env << 'EOF'
# 海纳数聚一体机配置
HAINAN_LLM_BASE_URL=http://192.168.3.86:18051/v1
HAINAN_LLM_MODEL=qwen3_30b_a3b
HAINAN_EMBED_BASE_URL=http://192.168.3.86:6208/v1
HAINAN_EMBED_MODEL=bce-embedding-base_v1

# 数据路径
DATA_DIR=/mnt/nas
STORAGE_DIR=/mnt/nas/raw
CLEANED_DIR=/mnt/nas/cleaned
EOF"

    log_success "服务器环境初始化完成"
}

#===============================================================================
# 启动清洗任务
#===============================================================================

cmd_start() {
    log_info "启动清洗任务..."

    # 首先同步最新代码
    sync_to_server

    # 构建启动命令
    WORKERS_OPT=""
    if [ -n "$CLEANING_WORKERS" ]; then
        WORKERS_OPT="--workers $CLEANING_WORKERS"
    fi

    START_CMD="cd ${REMOTE_PROJECT_DIR} && \
source venv/bin/activate && \
nohup bash scripts/run_cleaning.sh \
    --target /mnt/nas/cleaned \
    $WORKERS_OPT \
    --resume \
    > /mnt/nas/cleaned/logs/cleaning_$(date +%Y%m%d_%H%M%S).log 2>&1 &

echo '清洗任务已在后台启动'"

    remote_exec "$START_CMD"
    log_success "清洗任务已启动（后台运行）"
    log_info "查看日志: $0 logs"
}

#===============================================================================
# 停止清洗任务
#===============================================================================

cmd_stop() {
    log_warn "停止清洗任务..."

    remote_exec "pkill -f 'batch_processor.py' || echo '没有运行中的任务'"

    log_success "停止命令已发送"
}

#===============================================================================
# 查看任务状态
#===============================================================================

cmd_status() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  清洗任务状态${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    # 检查进程状态
    echo -e "${CYAN}运行中的进程:${NC}"
    remote_exec "ps aux | grep -E 'batch_processor|python.*cleaning' | grep -v grep || echo '  无运行中的任务'"

    echo ""

    # 检查 NAS 挂载
    echo -e "${CYAN}NAS 挂载状态:${NC}"
    remote_exec "echo '  /mnt/nas/raw:  ' && (mountpoint -q /mnt/nas/raw && echo '已挂载' || echo '未挂载')
echo '  /mnt/nas/cleaned: ' && (mountpoint -q /mnt/nas/cleaned && echo '已挂载' || echo '未挂载')"

    echo ""

    # 检查源文件数量
    echo -e "${CYAN}文件统计:${NC}"
    remote_exec "echo '  源目录文件数: ' && find /mnt/nas/raw -type f 2>/dev/null | wc -l
echo '  清洗后文件数: ' && find /mnt/nas/cleaned -name '*.json' 2>/dev/null | wc -l"

    echo ""

    # 查看最近日志
    echo -e "${CYAN}最近日志:${NC}"
    remote_exec "ls -lt /mnt/nas/cleaned/logs/*.log 2>/dev/null | head -1 | awk '{print '  最新日志: ' \$NF}'"
}

#===============================================================================
# 查看清洗进度
#===============================================================================

cmd_progress() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  清洗进度统计${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    remote_exec "cd ${REMOTE_PROJECT_DIR}
if [ -f '/mnt/nas/cleaned/.batch_progress.db' ]; then
    echo -e '${CYAN}数据库记录统计:${NC}'
    source venv/bin/activate
    python3 << 'PYEOF'
import sqlite3
import os

db_path = '/mnt/nas/cleaned/.batch_progress.db'
if not os.path.exists(db_path):
    print('进度数据库不存在')
    exit()

conn = sqlite3.connect(db_path)
cur = conn.execute('SELECT status, COUNT(*) FROM processed_files GROUP BY status')
results = list(cur)

total = sum(r[1] for r in results)
print(f'  总计记录: {total}')

for status, count in results:
    icon = '✓' if status == 'success' else ('⊘' if status == 'skipped' else '✗')
    pct = count / total * 100 if total > 0 else 0
    print(f'  {icon} {status}: {count} ({pct:.1f}%)')

# 查看最后处理的文件
cur = conn.execute('SELECT file_path, processed_at FROM processed_files ORDER BY processed_at DESC LIMIT 3')
print()
print('  最近处理的文件:')
for row in cur:
    print(f'    {row[0][:60]}... ({row[1]})')

conn.close()
PYEOF
else
    echo '  进度数据库不存在，请先启动清洗任务'
fi
"
}

#===============================================================================
# 查看日志
#===============================================================================

cmd_logs() {
    LINES=${1:-100}
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  清洗日志（最后 ${LINES} 行）${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""

    # 获取最新的日志文件
    LOG_FILE=$(remote_exec "ls -t /mnt/nas/cleaned/logs/*.log 2>/dev/null | head -1")

    if [ -z "$LOG_FILE" ]; then
        log_warn "没有找到日志文件"
        return
    fi

    log_info "日志文件: $LOG_FILE"
    echo ""

    remote_exec "tail -n $LINES '$LOG_FILE'"
}

#===============================================================================
# SSH 连接到服务器
#===============================================================================

cmd_ssh() {
    log_info "连接到服务器..."
    $SSH_CMD
}

#===============================================================================
# 帮助信息
#===============================================================================

show_help() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  远程任务管理脚本${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo "用法: $0 <命令>"
    echo ""
    echo -e "${GREEN}可用命令:${NC}"
    echo "  status      查看当前任务状态"
    echo "  start       启动清洗任务（后台运行）"
    echo "  stop        停止当前任务"
    echo "  progress    查看清洗进度统计"
    echo "  logs [n]    查看日志（默认最后100行）"
    echo "  ssh         打开 SSH 连接到服务器"
    echo "  setup       在服务器上初始化环境（首次使用）"
    echo "  sync        同步本地代码到服务器"
    echo "  help        显示此帮助信息"
    echo ""
    echo -e "${YELLOW}配置:${NC}"
    echo "  服务器: ${SERVER_USER}@${SERVER_HOST}:${SERVER_PORT}"
    echo "  项目路径: ${REMOTE_PROJECT_DIR}"
    echo ""
    echo -e "${YELLOW}示例:${NC}"
    echo "  $0 status           # 查看状态"
    echo "  $0 start            # 启动清洗"
    echo "  $0 logs 200         # 查看最后200行日志"
    echo ""
}

#===============================================================================
# 主入口
#===============================================================================

COMMAND=${1:-help}

case $COMMAND in
    status)
        cmd_status
        ;;
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    progress)
        cmd_progress
        ;;
    logs)
        cmd_logs $2
        ;;
    ssh)
        cmd_ssh
        ;;
    setup)
        cmd_setup
        ;;
    sync)
        sync_to_server
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "未知命令: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac
