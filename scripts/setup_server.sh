#!/bin/bash
#
# RAG 系统环境安装脚本
# 用途：在 Ubuntu 服务器上一键安装 MySQL、Qdrant、Python 环境
#
# 使用方法：
#   chmod +x setup_server.sh
#   ./setup_server.sh
#

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  RAG 系统环境安装脚本"
echo "=========================================="
echo ""

# ========== 1. 检测系统 ==========
echo "[1/7] 检测系统环境..."
if [[ ! -f /etc/os-release ]]; then
    echo "❌ 无法检测操作系统，请手动确认是 Ubuntu 22.04+"
    exit 1
fi

source /etc/os-release
echo "✓ 系统: $PRETTY_NAME"

# ========== 2. 更新系统 ==========
echo ""
echo "[2/7] 更新系统软件包..."
sudo apt update -qq
sudo apt upgrade -y -qq

# ========== 3. 安装 MySQL ==========
echo ""
echo "[3/7] 安装 MySQL..."
if command -v mysql &> /dev/null; then
    echo "✓ MySQL 已安装，跳过"
else
    echo "正在安装 MySQL Server..."
    sudo apt install -y mysql-server mysql-client

    # 启动 MySQL 并设置开机自启
    sudo systemctl start mysql
    sudo systemctl enable mysql

    # 等待 MySQL 启动
    sleep 3

    # 配置 MySQL root 密码
    echo "配置 MySQL root 密码..."
    sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'RagServer2024!';"
    sudo mysql -e "FLUSH PRIVILEGES;"

    # 创建数据库
    echo "创建数据库..."
    mysql -u root -p'RagServer2024!' -e "CREATE DATABASE IF NOT EXISTS rag_knowledge_base CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

    echo "✓ MySQL 安装完成"
fi

echo ""
echo "MySQL 配置信息："
echo "  主机: localhost"
echo "  端口: 3306"
echo "  用户: root"
echo "  密码: RagServer2024!"
echo "  数据库: rag_knowledge_base"

# ========== 4. 安装 Qdrant ==========
echo ""
echo "[4/7] 安装 Qdrant 向量数据库..."
if command -v qdrant &> /dev/null || [[ -d /opt/qdrant ]]; then
    echo "✓ Qdrant 已安装，跳过"
else
    echo "正在安装 Qdrant..."

    # 下载 Qdrant
    cd /tmp
    curl -LO https://github.com/qdrant/qdrant/releases/latest/download/qdrant-linux-x86_64.tar.gz

    # 创建目录并解压
    sudo mkdir -p /opt/qdrant
    sudo tar -xzf qdrant-linux-x86_64.tar.gz -C /opt/qdrant
    sudo ln -sf /opt/qdrant/qdrant /usr/local/bin/qdrant

    # 创建数据目录
    sudo mkdir -p /var/lib/qdrant

    # 创建 systemd 服务
    echo "创建 Qdrant 服务..."
    sudo tee /etc/systemd/system/qdrant.service > /dev/null <<'EOF'
[Unit]
Description=Qdrant Vector Database
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/qdrant --data-path /var/lib/qdrant --host 0.0.0.0 --port 6333
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    # 启动 Qdrant
    sudo systemctl daemon-reload
    sudo systemctl start qdrant
    sudo systemctl enable qdrant

    echo "✓ Qdrant 安装完成"
fi

echo ""
echo "Qdrant 配置信息："
echo "  地址: http://localhost:6333"
echo "  gRPC: localhost:6334"
echo "  数据目录: /var/lib/qdrant"

# ========== 5. 安装 Python 环境 ==========
echo ""
echo "[5/7] 安装 Python 环境..."
if command -v python3.10 &> /dev/null; then
    echo "✓ Python 3.10+ 已安装"
else
    echo "正在安装 Python 3.10..."
    sudo apt install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update -qq
    sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip git curl
fi

# 确保 python3 链接到 python3.10
if [[ ! -L /usr/bin/python3 ]]; then
    sudo ln -sf /usr/bin/python3.10 /usr/bin/python3
fi
if [[ ! -L /usr/bin/python ]]; then
    sudo ln -sf /usr/bin/python3.10 /usr/bin/python
fi

echo "✓ Python 版本:"
python3 --version

# ========== 6. 安装 Docker（可选，用于后续扩展）==========
echo ""
echo "[6/7] 检查 Docker（可选）..."
if command -v docker &> /dev/null; then
    echo "✓ Docker 已安装"
else
    echo "提示: Docker 未安装，如需容器化部署请运行："
    echo "  curl -fsSL https://get.docker.com | sh"
fi

# ========== 7. 防火墙配置 ==========
echo ""
echo "[7/7] 配置防火墙..."
if command -v ufw &> /dev/null; then
    echo "配置 ufw 防火墙..."
    sudo ufw allow 22/tcp    # SSH
    sudo ufw allow 3306/tcp  # MySQL（仅内网）
    sudo ufw allow 6333/tcp  # Qdrant（仅内网）
    sudo ufw allow 8001/tcp  # FastAPI（仅内网，如需公网访问请配置 VPN）
    sudo ufw --force enable
    echo "✓ 防火墙配置完成"
fi

# ========== 完成 ==========
echo ""
echo "=========================================="
echo "  环境安装完成！"
echo "=========================================="
echo ""
echo "下一步操作："
echo "1. 将 RAG 项目代码复制到服务器"
echo "2. 创建 Python 虚拟环境并安装依赖"
echo "3. 配置 .env 文件"
echo "4. 启动服务"
echo ""
echo "详细步骤请参考 scripts/SERVER_DEPLOY.md"
echo ""
