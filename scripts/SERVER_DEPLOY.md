# RAG 系统服务器部署指南

本文档详细说明如何在公司内网服务器上部署 RAG 系统并接入飞书机器人。

---

## 目录

1. [系统架构](#系统架构)
2. [服务器要求](#服务器要求)
3. [部署步骤](#部署步骤)
4. [飞书配置](#飞书配置)
5. [服务管理](#服务管理)
6. [故障排查](#故障排查)

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户设备                                  │
│                    (飞书 App / 浏览器)                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ 飞书协议 / HTTP
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      公司内网服务器                               │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                 │
│  │  FastAPI 服务     │    │    MySQL         │                 │
│  │  (端口 8001)      │    │  (端口 3306)     │                 │
│  │                   │    │                  │                 │
│  │  • 飞书 Webhook   │    │  • 员工信息      │                 │
│  │  • RAG API        │    │  • 会话历史      │                 │
│  │  • 文档上传       │    │  • 个人笔记      │                 │
│  └────────┬─────────┘    └────────┬─────────┘                 │
│           │                       │                             │
│           │                       │                             │
│           ▼                       ▼                             │
│  ┌──────────────────┐    ┌──────────────────┐                 │
│  │  Qdrant 向量库    │    │   海纳数聚      │                 │
│  │  (端口 6333)     │    │   一体机        │                 │
│  │                   │    │  (192.168.3.86) │                 │
│  │  • 向量存储       │    │                 │                 │
│  │  • 相似度检索    │    │  • LLM 模型     │                 │
│  │                   │    │  • Embedding   │                 │
│  │                   │    │  • Reranker   │                 │
│  └──────────────────┘    └──────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 服务器要求

### 最低配置
- CPU：4 核
- 内存：8 GB
- 硬盘：50 GB
- 网络：可访问一体机（192.168.3.x 网段）

### 推荐配置
- CPU：8 核
- 内存：16 GB
- 硬盘：100 GB
- 网络：千兆内网

### 软件要求
- 操作系统：Ubuntu 22.04 LTS
- Python：3.10+
- MySQL：8.0+
- Qdrant：最新版本

---

## 部署步骤

### 第一步：服务器基础环境

#### 1.1 创建 Ubuntu 虚拟机

使用 VMware/Hyper-V 创建虚拟机：
- 镜像：Ubuntu Server 22.04 LTS
- CPU：8 核
- 内存：16 GB
- 硬盘：100 GB
- 网络：桥接模式（与一体机同网段）

#### 1.2 安装基础环境

通过 SSH 连接到服务器，执行以下命令：

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y curl wget git unzip
```

### 第二步：运行一键安装脚本

将 `setup_server.sh` 复制到服务器，然后执行：

```bash
# 添加执行权限
chmod +x setup_server.sh

# 运行安装脚本
./setup_server.sh
```

此脚本会自动安装：
- MySQL 8.0
- Qdrant 向量数据库
- Python 3.10 环境

### 第三步：复制项目代码

#### 方式 A：使用 SCP（从本机复制）

```bash
# 在本机 PowerShell 中执行
scp -r C:\Users\huaci\Downloads\RAG-main\raguser@192.168.3.100:/home/raguser/
```

#### 方式 B：使用 Git

```bash
# 在服务器上执行
cd ~
git clone <your-git-repo-url> RAG-main
```

### 第四步：配置 Python 环境

```bash
# 进入项目目录
cd ~/RAG-main

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 安装文档处理依赖
pip install pymupdf python-docx openpyxl python-pptx
```

### 第五步：配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
nano .env
```

修改以下配置：

```bash
# MySQL 配置（使用安装脚本设置的密码）
MYSQL_PASSWORD=RagServer2024!

# 飞书配置（稍后从飞书开放平台获取）
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=your_feishu_app_secret_here

# 一体机配置（根据实际情况调整）
HAINAN_LLM_BASE_URL=http://192.168.3.86:18051/v1
HAINAN_EMBED_BASE_URL=http://192.168.3.86:6208/v1
HAINAN_RERANK_BASE_URL=http://192.168.3.86:6006/v1
```

### 第六步：测试一体机连接

```bash
# 测试 LLM 服务
curl -X POST http://192.168.3.86:18051/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3_30b_a3b", "messages": [{"role": "user", "content": "你好"}], "max_tokens": 10}'

# 测试 Embedding 服务
curl -X POST http://192.168.3.86:6208/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "bce-embedding-base_v1", "input": "测试文本"}'
```

### 第七步：启动服务

```bash
# 添加执行权限
chmod +x scripts/run_server.sh

# 启动服务
./scripts/run_server.sh start

# 查看状态
./scripts/run_server.sh status

# 查看日志
./scripts/run_server.sh logs
```

### 第八步：验证服务

```bash
# 健康检查
curl http://localhost:8001/health

# 应该返回
{"status":"ok","rag_engine":true,"history_manager":true}
```

---

## 飞书配置

详细步骤请参考 [FEISHU_CONFIG.md](FEISHU_CONFIG.md)

### 快速配置

1. 登录 [飞书开放平台](https://open.feishu.cn/app)
2. 创建企业自建应用
3. 获取 `App ID` 和 `App Secret`
4. 启用「机器人」能力
5. 配置事件订阅（Webhook URL）
6. 发布应用

### Webhook URL 格式

```
http://你的服务器IP:8001/feishu/webhook
```

例如：
```
http://192.168.3.100:8001/feishu/webhook
```

---

## 服务管理

### 基本命令

```bash
# 启动服务
./scripts/run_server.sh start

# 停止服务
./scripts/run_server.sh stop

# 重启服务
./scripts/run_server.sh restart

# 查看状态
./scripts/run_server.sh status

# 查看日志
./scripts/run_server.sh logs

# 实时查看日志
tail -f logs/app.log
```

### 设置开机自启

```bash
# 创建 systemd 服务
sudo tee /etc/systemd/system/rag-api.service > /dev/null <<EOF
[Unit]
Description=RAG API Service
After=network.target mysql.service qdrant.service

[Service]
Type=simple
User=raguser
WorkingDirectory=/home/raguser/RAG-main
ExecStart=/home/raguser/RAG-main/venv/bin/python /home/raguser/RAG-main/main.py --api
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 启用服务
sudo systemctl daemon-reload
sudo systemctl enable rag-api
sudo systemctl start rag-api

# 检查状态
sudo systemctl status rag-api
```

---

## 故障排查

### 服务无法启动

```bash
# 查看详细错误
journalctl -u rag-api -n 50

# 手动运行查看错误
cd ~/RAG-main
source venv/bin/activate
python main.py --api
```

### MySQL 连接失败

```bash
# 检查 MySQL 状态
sudo systemctl status mysql

# 测试连接
mysql -u root -p'RagServer2024!'

# 检查数据库
SHOW DATABASES;
USE rag_knowledge_base;
SHOW TABLES;
```

### Qdrant 连接失败

```bash
# 检查 Qdrant 状态
sudo systemctl status qdrant

# 检查端口
curl http://localhost:6333/collections
```

### 飞书机器人无响应

1. 确认 Webhook URL 可访问：
   ```bash
   curl http://你的服务器IP:8001/feishu/webhook
   ```

2. 检查飞书应用状态（需要在飞书开放平台确认）

3. 查看服务日志：
   ```bash
   ./scripts/run_server.sh logs | grep -i feishu
   ```

### 一体机连接失败

```bash
# 检查网络连通性
ping 192.168.3.86

# 检查端口
telnet 192.168.3.86 18051
```

---

## 后续维护

### 更新代码

```bash
# 停止服务
./scripts/run_server.sh stop

# 更新代码（如果使用 Git）
git pull

# 重新安装依赖
source venv/bin/activate
pip install -r requirements.txt

# 重启服务
./scripts/run_server.sh start
```

### 备份数据库

```bash
# 备份 MySQL
mysqldump -u root -p'RagServer2024!' rag_knowledge_base > backup_$(date +%Y%m%d).sql

# 备份 Qdrant
sudo systemctl stop qdrant
sudo tar -czf qdrant_backup_$(date +%Y%m%d).tar.gz /var/lib/qdrant
sudo systemctl start qdrant
```

---

## 联系支持

如有问题，请提供：
1. 服务器操作系统版本
2. 服务日志（`./scripts/run_server.sh logs`）
3. 错误截图
4. 最近的操作步骤
