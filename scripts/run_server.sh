#!/bin/bash
#
# RAG 系统启动脚本
# 用途：启动 FastAPI 服务（带日志和服务管理）
#
# 使用方法：
#   ./run_server.sh          # 启动服务
#   ./run_server.sh stop      # 停止服务
#   ./run_server.sh restart   # 重启服务
#   ./run_server.sh status    # 查看状态
#   ./run_server.sh logs      # 查看日志
#

set -e

# ========== 配置 ==========
APP_NAME="rag-api"
APP_PORT=8001
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$APP_DIR/logs"
PID_FILE="$APP_DIR/.rag_server.pid"
LOG_FILE="$LOG_DIR/app.log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# ========== 函数 ==========

start() {
    echo "启动 RAG API 服务..."

    # 检查是否已在运行
    if is_running; then
        echo "服务已在运行 (PID: $(cat $PID_FILE))"
        return 1
    fi

    # 进入应用目录
    cd "$APP_DIR"

    # 检查虚拟环境
    if [[ ! -d "venv" ]]; then
        echo "错误: 未找到虚拟环境 venv，请先运行 setup_server.sh"
        exit 1
    fi

    # 激活虚拟环境
    source venv/bin/activate

    # 检查配置文件
    if [[ ! -f ".env" ]]; then
        echo "警告: 未找到 .env 配置文件，将使用默认配置"
        echo "建议复制 .env.example 为 .env 并修改配置"
    fi

    # 后台启动服务
    nohup python main.py --api > "$LOG_FILE" 2>&1 &
    local pid=$!

    # 保存 PID
    echo $pid > "$PID_FILE"

    # 等待几秒检查是否启动成功
    sleep 3

    if is_running; then
        echo "✓ 服务启动成功 (PID: $pid)"
        echo "  API 地址: http://localhost:$APP_PORT"
        echo "  飞书 Webhook: http://YOUR_SERVER_IP:$APP_PORT/feishu/webhook"
        echo "  日志文件: $LOG_FILE"
    else
        echo "✗ 服务启动失败，请检查日志: $LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
}

stop() {
    echo "停止 RAG API 服务..."

    if [[ ! -f "$PID_FILE" ]]; then
        echo "服务未运行"
        return 1
    fi

    local pid=$(cat "$PID_FILE")

    if ps -p $pid > /dev/null 2>&1; then
        kill $pid
        sleep 2

        if ps -p $pid > /dev/null 2>&1; then
            echo "强制停止..."
            kill -9 $pid
        fi

        echo "✓ 服务已停止"
    else
        echo "服务未运行"
    fi

    rm -f "$PID_FILE"
}

restart() {
    stop
    sleep 2
    start
}

status() {
    if is_running; then
        local pid=$(cat "$PID_FILE")
        echo "✓ 服务正在运行 (PID: $pid)"

        # 检查端口
        if command -v ss &> /dev/null; then
            echo "  监听端口: $APP_PORT"
        fi

        # 显示最后几行日志
        if [[ -f "$LOG_FILE" ]]; then
            echo ""
            echo "最近日志:"
            tail -5 "$LOG_FILE"
        fi
    else
        echo "✗ 服务未运行"
    fi
}

logs() {
    if [[ -f "$LOG_FILE" ]]; then
        tail -50 "$LOG_FILE"
    else
        echo "日志文件不存在"
    fi
}

is_running() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE")
        ps -p $pid > /dev/null 2>&1
        return $?
    fi
    return 1
}

# ========== 主逻辑 ==========
case "${1:-start}" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    *)
        echo "用法: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
