#===============================================================================
# 远程服务器任务管理脚本 (Windows PowerShell)
# 用于从本机 Windows 管理虚拟机上的清洗任务
#
# 用法:
#   .\remote_manager.ps1 status      - 查看当前任务状态
#   .\remote_manager.ps1 start       - 启动清洗任务
#   .\remote_manager.ps1 stop        - 停止当前任务
#   .\remote_manager.ps1 logs [n]    - 查看日志（默认最后100行）
#   .\remote_manager.ps1 progress    - 查看清洗进度
#   .\remote_manager.ps1 ssh         - 打开 SSH 连接
#   .\remote_manager.ps1 setup       - 在服务器上初始化环境
#
# 首次使用请以管理员身份运行并修改配置区域
#===============================================================================

# ==================== 配置区域（请根据实际情况修改） ====================

# 虚拟机/服务器配置
$ServerHost = "192.168.3.100"          # 服务器IP（请修改）
$ServerUser = "your_username"           # 服务器用户名（请修改）
$ServerPort = 22                        # SSH端口（默认22）

# 服务器上的项目路径
$RemoteProjectDir = "/opt/rag-cleaner"

# NAS 配置
$NasRawPath = "/mnt/nas/raw"           # 原始数据路径
$NasCleanedPath = "/mnt/nas/cleaned"   # 清洗后数据路径

# 清洗参数
$CleaningWorkers = ""                   # 留空使用默认，或指定如 "8"
$CleaningBatchSize = 20

# ==================== 辅助函数 ====================

function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "[SUCCESS] $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

function Remote-Exec {
    param([string]$Command)
    ssh -p $ServerPort "$ServerUser@$ServerHost" $Command
}

function Get-LogFile {
    Remote-Exec "ls -t /mnt/nas/cleaned/logs/*.log 2>/dev/null | head -1"
}

# ==================== 命令实现 ====================

function Show-Help {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  远程任务管理脚本" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "用法: .\remote_manager.ps1 <命令>"
    Write-Host ""
    Write-Host "可用命令:" -ForegroundColor Green
    Write-Host "  status      查看当前任务状态"
    Write-Host "  start       启动清洗任务（后台运行）"
    Write-Host "  stop        停止当前任务"
    Write-Host "  progress    查看清洗进度统计"
    Write-Host "  logs [n]    查看日志（默认最后100行）"
    Write-Host "  ssh         打开 SSH 连接到服务器"
    Write-Host "  setup       在服务器上初始化环境（首次使用）"
    Write-Host "  sync        同步本地代码到服务器"
    Write-Host "  help        显示此帮助信息"
    Write-Host ""
    Write-Host "配置:" -ForegroundColor Yellow
    Write-Host "  服务器: ${ServerUser}@${ServerHost}:${ServerPort}"
    Write-Host "  项目路径: $RemoteProjectDir"
    Write-Host ""
}

function Cmd-Status {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  清洗任务状态" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "运行中的进程:" -ForegroundColor Magenta
    Remote-Exec "ps aux | grep -E 'batch_processor|python.*cleaning' | grep -v grep || echo '无运行中的任务'"
    Write-Host ""

    Write-Host "NAS 挂载状态:" -ForegroundColor Magenta
    Remote-Exec @"
echo "  $NasRawPath:   " && (mountpoint -q $NasRawPath && echo '已挂载' || echo '未挂载')
echo "  $NasCleanedPath: " && (mountpoint -q $NasCleanedPath && echo '已挂载' || echo '未挂载')
"@

    Write-Host ""
    Write-Host "文件统计:" -ForegroundColor Magenta
    Remote-Exec @"
echo "  源目录文件数: " && find $NasRawPath -type f 2>/dev/null | wc -l
echo "  清洗后文件数: " && find $NasCleanedPath -name '*.json' 2>/dev/null | wc -l
"@

    Write-Host ""
    Write-Host "最近日志:" -ForegroundColor Magenta
    $latestLog = Get-LogFile
    if ($latestLog) {
        Write-Host "  最新日志: $latestLog"
    } else {
        Write-Host "  没有找到日志文件"
    }
}

function Cmd-Progress {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  清洗进度统计" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    Remote-Exec @"
cd $RemoteProjectDir
if [ -f '$NasCleanedPath/.batch_progress.db' ]; then
    echo '进度数据库统计:'
    source venv/bin/activate
    python3 << 'PYEOF'
import sqlite3
import os

db_path = '$NasCleanedPath/.batch_progress.db'
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
conn.close()
PYEOF
else
    echo '进度数据库不存在，请先启动清洗任务'
fi
"@
}

function Cmd-Logs {
    param([int]$Lines = 100)

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "  清洗日志（最后 ${Lines} 行）" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    $logFile = Get-LogFile
    if (-not $logFile) {
        Write-Warn "没有找到日志文件"
        return
    }

    Write-Info "日志文件: $logFile"
    Write-Host ""
    Remote-Exec "tail -n $Lines '$logFile'"
}

function Cmd-Start {
    Write-Info "启动清洗任务..."

    # 同步代码
    Write-Info "同步本地代码到服务器..."
    $localPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projectRoot = Split-Path -Parent $localPath
    $excludeOpts = "--exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' --exclude='.venv'"
    Remote-Exec "mkdir -p $RemoteProjectDir"
    rsync -avz -e "ssh -p $ServerPort" $excludeOpts "$projectRoot/" "$ServerUser@$ServerHost`:$RemoteProjectDir/"

    # 构建启动命令
    $workersOpt = if ($CleaningWorkers) { "--workers $CleaningWorkers" } else { "" }
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

    $startCmd = @"
cd $RemoteProjectDir && \
source venv/bin/activate && \
nohup bash scripts/run_cleaning.sh \
    --target $NasCleanedPath \
    $workersOpt \
    --resume \
    > $NasCleanedPath/logs/cleaning_${timestamp}.log 2>&1 &
echo '清洗任务已在后台启动'
"@

    Remote-Exec $startCmd
    Write-Success "清洗任务已启动（后台运行）"
    Write-Info "查看进度: .\remote_manager.ps1 progress"
    Write-Info "查看日志: .\remote_manager.ps1 logs"
}

function Cmd-Stop {
    Write-Warn "停止清洗任务..."
    Remote-Exec "pkill -f 'batch_processor.py' || echo '没有运行中的任务'"
    Write-Success "停止命令已发送"
}

function Cmd-SSH {
    Write-Info "连接到服务器..."
    ssh -p $ServerPort "$ServerUser@$ServerHost"
}

function Cmd-Setup {
    Write-Info "初始化服务器环境..."

    # 创建目录
    Remote-Exec @"
mkdir -p $RemoteProjectDir
mkdir -p $NasRawPath
mkdir -p $NasCleanedPath
mkdir -p $NasCleanedPath/logs
"@

    # 同步代码
    Write-Info "同步本地代码到服务器..."
    $localPath = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projectRoot = Split-Path -Parent $localPath
    $excludeOpts = "--exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='venv' --exclude='.venv'"
    rsync -avz -e "ssh -p $ServerPort" $excludeOpts "$projectRoot/" "$ServerUser@$ServerHost`:$RemoteProjectDir/"

    # 安装依赖
    Write-Info "安装 Python 依赖..."
    Remote-Exec @"
cd $RemoteProjectDir
if [ ! -d 'venv' ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pymupdf python-docx openpyxl python-pptx
"@

    # 创建配置文件
    Write-Info "创建配置文件..."
    Remote-Exec @"
cat > $RemoteProjectDir/.env << 'EOF'
# 海纳数聚一体机配置
HAINAN_LLM_BASE_URL=http://192.168.3.86:18051/v1
HAINAN_LLM_MODEL=qwen3_30b_a3b
HAINAN_EMBED_BASE_URL=http://192.168.3.86:6208/v1
HAINAN_EMBED_MODEL=bce-embedding-base_v1

# 数据路径
DATA_DIR=/mnt/nas
STORAGE_DIR=$NasRawPath
CLEANED_DIR=$NasCleanedPath
EOF
"@

    Write-Success "服务器环境初始化完成"
}

# ==================== 主入口 ====================

$Command = $args[0]

switch ($Command) {
    "status" { Cmd-Status }
    "start" { Cmd-Start }
    "stop" { Cmd-Stop }
    "progress" { Cmd-Progress }
    "logs" { Cmd-Logs -Lines ([int]$args[1]) }
    "ssh" { Cmd-SSH }
    "setup" { Cmd-Setup }
    "help" { Show-Help }
    { $_ -eq $null -or $_ -eq "" } { Show-Help }
    default {
        Write-Err "未知命令: $_"
        Write-Host ""
        Show-Help
        exit 1
    }
}
