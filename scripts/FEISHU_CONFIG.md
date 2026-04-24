# 飞书机器人配置指南

本文档说明如何在飞书开放平台配置机器人，并将其接入 RAG 系统。

---

## 一、前置准备

### 1. 确认服务器已部署

在配置飞书之前，请确保：
- RAG 服务已部署到服务器
- 服务可以正常访问
- 服务器有公网 IP 或可通过内网穿透访问

### 2. 确认 Webhook 地址

飞书需要访问你的服务器 Webhook URL，格式为：
```
http://你的服务器IP:8001/feishu/webhook
```

如果你的服务器没有公网 IP，需要配置内网穿透：
- 使用 frp：https://github.com/fatedier/frp
- 使用 ngrok：https://ngrok.com
- 使用花生壳等内网穿透工具

---

## 二、飞书开放平台配置

### 1. 创建应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击「创建企业自建应用」
3. 填写应用信息：
   - 应用名称：如「RAG 知识助手」
   - 应用描述：企业内部知识库问答机器人
   - 应用图标：可上传自定义图标
4. 点击「创建应用」

### 2. 获取凭证

1. 进入应用详情页
2. 点击「凭证与基础信息」
3. 复制以下信息：
   - `App ID`：如 `cli_xxxxxxxxxxxxxxxx`
   - `App Secret`：点击查看复制

### 3. 配置机器人能力

1. 在左侧菜单选择「添加应用能力」
2. 找到「机器人」并点击添加
3. 启用机器人功能

### 4. 配置权限

1. 在左侧菜单选择「权限管理」
2. 添加以下权限：

| 权限名称 | 权限标识 |
|---------|---------|
| 获取用户基本信息 | contact:user.employee_id:readonly |
| 获取部门用户列表 | contact:user.base:readonly |
| 获取部门信息 | contact:department.base:readonly |
| 发送消息到群组 | im:message:send_as_bot |
| 接收消息 | im:message:receive_v1 |
| 使用多维表格 | bitable:app:readonly |

### 5. 配置事件订阅

1. 在左侧菜单选择「事件与回调」
2. 点击「事件配置」
3. 设置「事件配置」页面：
   - **请求地址**：填写你的 Webhook URL
     ```
     http://你的服务器IP:8001/feishu/webhook
     ```
   - **加密密钥**：可以留空或填写自定义密钥
   - **签名密钥**：可以留空或填写自定义密钥

4. 添加订阅事件：
   - `im.message.receive_v1`（接收消息）

### 6. 发布应用

1. 在左侧菜单选择「版本管理与发布」
2. 点击「创建版本」
3. 填写版本信息并提交
4. 联系企业管理员审批（如果是自建应用可能需要）

---

## 三、配置 RAG 系统

### 1. 修改 .env 配置

在服务器上的 `.env` 文件中配置飞书信息：

```bash
# 飞书 Bot 配置
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=your_app_secret_here
FEISHU_VERIFICATION_TOKEN=your_verification_token_here  # 可选
```

### 2. 重启服务

```bash
# 停止服务
./scripts/run_server.sh stop

# 启动服务
./scripts/run_server.sh start

# 查看日志确认启动成功
./scripts/run_server.sh logs
```

### 3. 验证服务

测试 Webhook 是否可达：

```bash
# 在本地测试服务器是否可达
curl http://你的服务器IP:8001/health

# 应该返回
{"status":"ok","rag_engine":true,"history_manager":true}
```

---

## 四、测试机器人

### 1. 添加机器人到会话

1. 在飞书中打开任意会话
2. 点击右上角「...」→「添加机器人」
3. 选择你创建的「RAG 知识助手」

### 2. 发送测试消息

发送以下命令测试：

```
帮助
```

如果机器人回复帮助信息，说明配置成功。

---

## 五、常见问题

### Q: 机器人无响应

1. 检查服务器日志：`./scripts/run_server.sh logs`
2. 确认 Webhook URL 可访问
3. 确认飞书应用已发布
4. 检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 是否正确

### Q: Webhook URL 无法访问

如果服务器在内网，需要配置内网穿透：

```bash
# 使用 frp 配置示例（客户端）
# 在有公网 IP 的机器上运行 frps
./frps -c frps.ini

# 在 RAG 服务器上运行 frpc
./frpc -c frpc.ini
```

frpc.ini 配置示例：
```ini
[feishu_webhook]
type = tcp
local_ip = 127.0.0.1
local_port = 8001
remote_port = 8001
```

### Q: 消息发送失败

1. 检查飞书应用权限是否包含消息发送权限
2. 确认应用已发布并被用户添加

---

## 六、机器人命令

配置成功后，用户可以发送以下命令：

| 命令 | 说明 |
|-----|------|
| `帮助` / `help` | 查看所有命令 |
| `开启赛博员工` | 启用个人知识库功能 |
| `关闭赛博员工` | 关闭个人知识库功能 |
| `创建笔记` + 内容 | 创建个人笔记 |
| `查看笔记` | 查看笔记列表 |
| `搜索笔记 + 关键词` | 搜索笔记 |
| `我的知识图谱` | 查看个人知识图谱 |
| `我的记忆` | 查看个人记忆 |

或者直接提问，机器人会从知识库检索回答。
