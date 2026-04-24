# NAS 数据清洗 - 部署指南

本文档说明如何利用海纳数聚AI大模型一体机的算力，对NAS中的原始数据进行清洗处理。

---

## 整体架构

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   您的本机       │     │   服务器          │     │   海纳数聚一体机     │
│  (开发/管理)     │ ──> │  Linux虚拟机      │ ──> │   (LLM + Embedding) │
│                 │     │  - 挂载NAS       │     │   192.168.3.86      │
│                 │     │  - 运行清洗脚本   │     │                     │
└─────────────────┘     └────────┬─────────┘     └─────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │         NAS存储           │
                    │  /mnt/nas/raw → 原始数据  │
                    │  /mnt/nas/cleaned → 清洗后│
                    └─────────────────────────┘
```

---

## 前置条件

### 1. 服务器要求
- 可创建 Linux 虚拟机（推荐 Ubuntu 22.04 LTS）
- 虚拟机配置：建议 8核+ CPU, 16GB+ 内存
- 虚拟机可访问 NAS 存储

### 2. 网络配置
- 虚拟机可访问 NAS（如 192.168.x.x）
- 虚拟机可访问一体机（如 192.168.3.86）
- 建议虚拟机与一体机在同一网段

### 3. 一体机服务确认
确认一体机已开启以下服务：
- LLM 服务：`http://192.168.3.86:18051/v1`
- Embedding 服务：`http://192.168.3.86:6208/v1`
- Reranker 服务：`http://192.168.3.86:6006/v1`

---

## 步骤一：在服务器上创建 Linux 虚拟机

### 使用 VMware/Hyper-V 创建虚拟机

1. **创建新虚拟机**
   - 类型：Ubuntu 22.04 LTS Server
   - CPU：8 核
   - 内存：16 GB
   - 硬盘：100 GB（根据数据量调整）
   - 网络：桥接模式（与一体机同网段）

2. **安装 Ubuntu Server**
   - 安装时勾选 "OpenSSH Server"
   - 设置固定 IP（如 192.168.3.100）

3. **更新系统**
```bash
sudo apt update && sudo apt upgrade -y
```

---

## 步骤二：配置 NAS 挂载

### 方案 A：NFS 挂载（推荐）

```bash
# 1. 安装 NFS 客户端
sudo apt install -y nfs-common

# 2. 创建挂载点
sudo mkdir -p /mnt/nas/raw
sudo mkdir -p /mnt/nas/cleaned

# 3. 挂载 NAS（根据您的NAS地址修改）
# 原始数据目录
sudo mount -t nfs 192.168.x.x:/nas/raw /mnt/nas/raw
# 清洗后数据目录
sudo mount -t nfs 192.168.x.x:/nas/cleaned /mnt/nas/cleaned

# 4. 设置开机自动挂载
echo "192.168.x.x:/nas/raw /mnt/nas/raw nfs defaults 0 0" | sudo tee -a /etc/fstab
echo "192.168.x.x:/nas/cleaned /mnt/nas/cleaned nfs defaults 0 0" | sudo tee -a /etc/fstab
```

### 方案 B：SMB/CIFS 挂载

```bash
# 1. 安装 SMB 客户端
sudo apt install -y cifs-utils

# 2. 创建凭据文件（安全）
sudo nano /root/.smbcredentials
# 文件内容：
# username=your_nas_user
# password=your_nas_password

sudo chmod 600 /root/.smbcredentials

# 3. 挂载
sudo mount -t cifs //192.168.x.x/nas_raw /mnt/nas/raw -o credentials=/root/.smbcredentials,iocharset=utf8
sudo mount -t cifs //192.168.x.x/nas_cleaned /mnt/nas/cleaned -o credentials=/root/.smbcredentials,iocharset=utf8
```

### 方案 C：如果 NAS 直接挂载在服务器上

```bash
# 直接映射现有挂载点
sudo ln -s /mnt/your_nas_mount /mnt/nas
```

---

## 步骤三：在虚拟机上部署清洗环境

### 1. 安装 Python 和依赖

```bash
# 安装 Python 3.10+
sudo apt install -y python3.10 python3.10-venv python3-pip git

# 创建项目目录
mkdir -p /opt/rag-cleaner
cd /opt/rag-cleaner

# 克隆或复制项目（从本机复制）
# 方式1：使用 scp 从本机复制
scp -r user@your_local_ip:/path/to/RAG-main/* ./

# 方式2：使用 Git（如果有仓库）
git clone <your_repo_url> .
```

### 2. 安装 Python 依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 安装 PDF 处理依赖
pip install pymupdf python-docx openpyxl python-pptx
```

### 3. 配置环境变量

```bash
# 创建 .env 文件
cat > .env << 'EOF'
# 海纳数聚一体机配置
HAINAN_LLM_BASE_URL=http://192.168.3.86:18051/v1
HAINAN_LLM_MODEL=qwen3_30b_a3b
HAINAN_EMBED_BASE_URL=http://192.168.3.86:6208/v1
HAINAN_EMBED_MODEL=bce-embedding-base_v1

# 数据路径（虚拟机上的挂载点）
DATA_DIR=/mnt/nas
STORAGE_DIR=/mnt/nas/raw
CLEANED_DIR=/mnt/nas/cleaned
EOF
```

---

## 步骤四：测试连接

### 测试一体机连接

```bash
# 测试 LLM 服务
curl -X POST http://192.168.3.86:18051/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3_30b_a3b", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 10}'

# 测试 NAS 访问
ls -la /mnt/nas/raw
ls -la /mnt/nas/cleaned
```

---

## 步骤五：执行清洗

### 方式一：直接运行

```bash
cd /opt/rag-cleaner
source venv/bin/activate

python parsers/batch_processor.py \
  --source /mnt/nas/raw \
  --target /mnt/nas/cleaned \
  --workers 8 \
  --batch-size 20 \
  --resume
```

### 方式二：使用一键脚本

```bash
cd /opt/rag-cleaner
chmod +x scripts/run_cleaning.sh
./scripts/run_cleaning.sh
```

### 方式三：后台运行（长时间任务）

```bash
# 使用 nohup 后台运行
nohup bash scripts/run_cleaning.sh > cleaning.log 2>&1 &

# 查看进度
tail -f cleaning.log

# 查看进程
ps aux | grep batch_processor
```

---

## 步骤六：监控和管理

### 查看清洗进度

```bash
# 查看实时日志
tail -f /mnt/nas/cleaned/logs/batch_*.log

# 查看进度数据库统计
python -c "
import sqlite3
conn = sqlite3.connect('/mnt/nas/cleaned/.batch_progress.db')
cur = conn.execute('SELECT status, COUNT(*) FROM processed_files GROUP BY status')
for row in cur: print(f'{row[0]}: {row[1]}')
conn.close()
"

# 查看已清洗文件数量
ls /mnt/nas/cleaned/*.json | wc -l
```

### 常见运维操作

```bash
# 1. 强制重新处理所有文件（删除进度数据库）
rm /mnt/nas/cleaned/.batch_progress.db
python parsers/batch_processor.py --source /mnt/nas/raw --target /mnt/nas/cleaned --workers 8

# 2. 只扫描不处理（查看待处理文件）
python parsers/batch_processor.py --source /mnt/nas/raw --target /mnt/nas/cleaned --scan-only

# 3. 排除特定目录
python parsers/batch_processor.py --source /mnt/nas/raw --target /mnt/nas/cleaned \
  --exclude-dir temp --exclude-dir backup --exclude-dir .git

# 4. 中断后继续（自动断点续传）
python parsers/batch_processor.py --source /mnt/nas/raw --target /mnt/nas/cleaned --resume
```

---

## 从本机远程管理

### 使用 SSH 远程执行命令

```bash
# 从本机 SSH 连接到虚拟机
ssh user@192.168.3.100

# 或直接执行单个命令
ssh user@192.168.3.100 "cd /opt/rag-cleaner && source venv/bin/activate && python parsers/batch_processor.py --source /mnt/nas/raw --target /mnt/nas/cleaned --scan-only"
```

### 使用远程任务管理脚本

```bash
# 在本机上编辑脚本配置
# 修改 scripts/remote_manager.sh 中的服务器信息

# 执行远程清洗
./scripts/remote_manager.sh start

# 查看远程状态
./scripts/remote_manager.sh status

# 查看远程日志
./scripts/remote_manager.sh logs
```

---

## 故障排查

### 1. NAS 挂载失败
```bash
# 检查 NAS 服务是否可用
showmount -e 192.168.x.x

# 查看挂载错误
dmesg | tail -20
```

### 2. 一体机连接失败
```bash
# 检查网络连通性
ping 192.168.3.86

# 检查端口是否开放
telnet 192.168.3.86 18051
```

### 3. Python 依赖问题
```bash
# 重新安装依赖
pip install --force-reinstall -r requirements.txt
```

### 4. 内存不足
```bash
# 查看内存使用
free -h

# 增加 swap
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 性能优化建议

1. **增加并发数**：根据 CPU 核心数调整 `--workers` 参数
   - 8核CPU：建议 `--workers 7`
   - 16核CPU：建议 `--workers 15`

2. **调整批大小**：根据文件平均大小调整
   - 小文件（<1MB）：`--batch-size 50`
   - 大文件（>10MB）：`--batch-size 10`

3. **使用 SSD 存储进度数据库**：将 `.batch_progress.db` 放在本地 SSD 上

4. **网络优化**：确保虚拟机与 NAS、一体机在同一个交换机下

---

## 安全建议

1. **NAS 凭据**：不要将 NAS 密码明文保存，使用 `/root/.smbcredentials`
2. **防火墙**：只开放必要的端口
3. **定期备份**：定期备份进度数据库

---

## 联系方式

如有问题，请检查：
1. `parsers/batch_processor.py` 的日志输出
2. 一体机的服务状态
3. NAS 的访问权限
