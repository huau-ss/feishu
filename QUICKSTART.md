# 快速开始指南

本文档帮助您快速搭建环境并开始数据清洗。

---

## 一分钟概览

```
┌─────────────────────────────────────────────────────────────┐
│  您的需求                                                  │
│  • NAS 中有大量原始数据                                     │
│  • 需要用一体机的算力进行清洗                                │
│  • 清洗后的数据存回 NAS 的另一个区域                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  解决方案                                                  │
│  服务器(VM) ──挂载──> NAS ──> 清洗脚本 ──> 清洗后数据      │
│      │                                                    │
│      └──一体机(算力)                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 第一步：在服务器上创建 Linux 虚拟机

### 图形化方式（推荐新手）

1. **打开虚拟机软件**（VMware Workstation / Hyper-V / VirtualBox）

2. **创建新虚拟机**
   - 选择：Ubuntu Server 22.04 LTS（.iso 文件）
   - CPU：8 核
   - 内存：16 GB
   - 硬盘：100 GB
   - 网络：桥接模式

3. **安装 Ubuntu**
   - 用户名：`raguser`
   - 密码：请设置强密码
   - 勾选：安装 OpenSSH Server

4. **设置固定 IP**
   ```bash
   # 编辑网络配置
   sudo nano /etc/netplan/00-installer-config.yaml

   # 修改为类似以下内容（根据您的网络调整）
   network:
     ethernets:
       ens33:
         addresses: [192.168.3.100/24]
         gateway4: 192.168.3.1
         nameservers:
           addresses: [8.8.8.8, 8.8.4.4]
     version: 2

   # 应用配置
   sudo netplan apply
   ```

5. **更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

## 第二步：复制项目到虚拟机

### 方式 A：使用 WinSCP（可视化）

1. 下载 WinSCP：https://winscp.net/
2. 连接虚拟机：`raguser@192.168.3.100`
3. 把 `RAG-main` 文件夹拖到 `/home/raguser/`

### 方式 B：使用 SCP 命令

```powershell
# 在本机 PowerShell 中执行
scp -r C:\Users\huaci\Downloads\RAG-main\raguser@192.168.3.100:/home/raguser/RAG-main
```

---

## 第三步：配置 NAS 挂载

### 在虚拟机中执行

```bash
# 连接到虚拟机
ssh raguser@192.168.3.100

# 进入项目目录
cd ~/RAG-main/scripts

# 给脚本添加执行权限
chmod +x mount_nas.sh

# 运行挂载脚本（交互式）
sudo ./mount_nas.sh
```

### 按照提示输入

```
请选择 NAS 挂载类型:
  1) NFS（推荐，用于 Linux 服务器）
  2) SMB/CIFS（用于 Windows NAS 或混合环境）

请选择 [1/2]: 1          # 根据您的 NAS 类型选择
NAS IP 地址: 192.168.x.x  # 您的 NAS IP
NAS 上原始数据路径: /volume1/raw
NAS 上清洗后数据路径: /volume1/cleaned
```

---

## 第四步：安装 Python 环境

```bash
# 连接到虚拟机
ssh raguser@192.168.3.100

# 进入项目目录
cd ~/RAG-main

# 安装系统依赖
sudo apt install -y python3.10 python3.10-venv python3-pip git

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装 Python 依赖
pip install --upgrade pip
pip install -r requirements.txt

# 安装文档处理依赖
pip install pymupdf python-docx openpyxl python-pptx

# 创建配置文件
cat > .env << 'EOF'
HAINAN_LLM_BASE_URL=http://192.168.3.86:18051/v1
HAINAN_LLM_MODEL=qwen3_30b_a3b
HAINAN_EMBED_BASE_URL=http://192.168.3.86:6208/v1
HAINAN_EMBED_MODEL=bce-embedding-base_v1
EOF
```

---

## 第五步：测试一体机连接

```bash
# 在虚拟机中测试
curl -X POST http://192.168.3.86:18051/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3_30b_a3b", "messages": [{"role": "user", "content": "你好"}], "max_tokens": 10}'
```

如果返回正常响应，说明一体机连接正常。

---

## 第六步：执行清洗

### 方式一：扫描（先看看有多少文件）

```bash
cd ~/RAG-main
source venv/bin/activate

python parsers/batch_processor.py \
  --source /mnt/nas/raw \
  --target /mnt/nas/cleaned \
  --scan-only
```

### 方式二：开始清洗

```bash
cd ~/RAG-main
source venv/bin/activate

# 开始清洗（8个并发进程）
python parsers/batch_processor.py \
  --source /mnt/nas/raw \
  --target /mnt/nas/cleaned \
  --workers 8 \
  --batch-size 20 \
  --resume
```

### 方式三：使用一键脚本

```bash
cd ~/RAG-main
chmod +x scripts/run_cleaning.sh
./scripts/run_cleaning.sh --workers 8 --resume
```

---

## 从本机远程管理

### 安装远程管理脚本（在 Windows 本机）

1. 编辑 `scripts/remote_manager.ps1` 中的配置：
   ```powershell
   $ServerHost = "192.168.3.100"      # 您的虚拟机 IP
   $ServerUser = "raguser"            # 您的用户名
   ```

2. 在 PowerShell 中使用：
   ```powershell
   # 查看状态
   .\scripts\remote_manager.ps1 status

   # 查看进度
   .\scripts\remote_manager.ps1 progress

   # 查看日志
   .\scripts\remote_manager.ps1 logs
   ```

---

## 常用命令速查

| 操作 | 命令 |
|------|------|
| 查看清洗进度 | `sqlite3 /mnt/nas/cleaned/.batch_progress.db "SELECT status, COUNT(*) FROM processed_files GROUP BY status"` |
| 查看已清洗文件数 | `ls /mnt/nas/cleaned/*.json \| wc -l` |
| 强制重新处理 | `rm /mnt/nas/cleaned/.batch_progress.db && python parsers/batch_processor.py ...` |
| 停止清洗 | `pkill -f batch_processor` |
| 查看实时日志 | `tail -f /mnt/nas/cleaned/logs/batch_*.log` |

---

## 常见问题

### Q: NAS 挂载失败

```bash
# 检查 NAS 是否可达
ping 192.168.x.x

# 检查 NFS 服务
showmount -e 192.168.x.x
```

### Q: 一体机连接失败

```bash
# 检查网络
ping 192.168.3.86

# 检查端口
telnet 192.168.3.86 18051
```

### Q: 内存不足

```bash
# 查看内存
free -h

# 增加 swap
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 下一步

- 查看 `DEPLOYMENT_GUIDE.md` 获取更详细的部署说明
- 查看 `README.md` 了解项目结构
