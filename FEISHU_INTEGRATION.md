# 飞书个性化 Bot 接入指南

## 概述

本系统支持为每个员工配置专属的 AI 问答 Bot，通过飞书即时通讯平台提供个性化服务。

核心特性：
- **多 Skill 模板**：为不同类型员工预设不同的回答风格
- **自动注册**：员工首次发消息时自动注册
- **RAG 增强**：基于企业知识库提供准确的回答
- **会话管理**：追踪每个员工的对话历史
- **管理后台**：HR/管理员通过 Streamlit 管理员工和 Skill

---

## 快速开始

### 第一步：创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击「创建企业自建应用」
3. 填写应用名称（建议：`AI 知识助手`）和描述
4. 点击创建，进入应用详情页

### 第二步：启用机器人能力

1. 在应用详情页，点击「添加应用能力」
2. 选择「机器人」，点击启用

### 第三步：配置事件订阅

1. 进入「事件与回调」→「事件订阅」
2. 点击「添加事件」，搜索并添加 `im.message.receive_v1`（接收消息）
3. 在「事件配置」中填写**请求地址 URL**：

```
https://your-domain.com/feishu/webhook
```

> 注意：`your-domain.com` 需要是公网可访问的域名。如果是本地开发，可以使用内网穿透工具（如 ngrok）进行测试。

4. 获取并保存**事件订阅 Verification Token**

### 第四步：获取应用凭证

1. 进入「凭证与基础信息」
2. 复制 **App ID** 和 **App Secret**

### 第五步：配置环境变量

在项目根目录的 `.env` 文件中添加：

```env
# 飞书 Bot 配置
FEISHU_APP_ID=cli_xxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxx
FEISHU_VERIFICATION_TOKEN=xxxxxxxxxxxxxxxxxxxxxx
```

### 第六步：启动服务

```bash
# 启动 API 服务
python main.py --api

# 在另一个终端启动飞书管理后台（可选）
python main.py --feishu-admin
```

### 第七步：发布应用

1. 在「版本管理与发布」中创建版本
2. 选择发布范围（建议先在测试范围发布）
3. 等待审核通过（或在企业内直接启用）

---

## 架构说明

```
飞书用户消息
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  FastAPI (/feishu/webhook)                          │
│  1. URL 验证 (GET /feishu/webhook)                  │
│  2. 消息接收 (POST /feishu/webhook)                 │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  FeishuBot.handle_message()                         │
│  1. 解析消息 → FeishuMessage                        │
│  2. 频率限制检查                                    │
│  3. 员工查找/注册 (EmployeeManager)                 │
│  4. Skill 获取 (SkillManager)                       │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  SkillTemplateEngine.build_personalized_prompt()     │
│  根据员工 Skill 构建个性化系统提示词                  │
│  - 回答风格 (严谨/高效/新人友好)                     │
│  - LLM 参数 (temperature, max_tokens)              │
│  - 知识范围过滤器                                    │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  RAG Engine.query() + 个性化 Prompt                 │
│  1. 知识库检索                                      │
│  2. Reranker 精排                                   │
│  3. LLM 生成                                        │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  FeishuClient 发送回复                              │
│  - 交互式卡片消息 (Interactive Card)                 │
│  - 包含回答内容 + 参考来源                            │
└─────────────────────────────────────────────────────┘
```

---

## Skill 模板系统

### 内置 Skill

系统默认创建 4 个 Skill 模板：

| Skill | 风格 | 适用人群 | 特点 |
|-------|------|----------|------|
| `skill_rigorous` | 严谨型 🔬 | 严谨型员工 | 详细、有逻辑、引用来源、步骤完整 |
| `skill_efficient` | 高效型 ⚡ | 高智型员工 | 框架式、点到为止、给方向而非给答案 |
| `skill_beginner` | 新人友好型 🌱 | 新人员工 | 通俗易懂、带比喻、日常化解释 |
| `skill_default` | 平衡型 ⚖️ | 默认 | 标准风格，适合大多数场景 |

### 创建自定义 Skill

通过管理后台（`python main.py --feishu-admin`）或 API 创建：

```bash
curl -X POST http://localhost:8001/admin/skills \
  -H "Content-Type: application/json" \
  -d '{
    "name": "财务分析型",
    "description": "适合财务人员，注重数据准确性和合规性",
    "answer_style": "rigorous",
    "temperature": 0.3,
    "max_tokens": 3000,
    "system_prompt_suffix": "你是一位专业的财务顾问...\n回答要注重数据准确性...\n包含合规风险提示...",
    "knowledge_scope": ["财务报表", "税务法规", "成本分析"],
    "priority": 8
  }'
```

### 为员工绑定 Skill

```bash
# 手动注册员工
curl -X POST http://localhost:8001/admin/employees \
  -H "Content-Type: application/json" \
  -d '{
    "feishu_user_id": "ou_xxxxxxxxxxxxx",
    "name": "张三",
    "department": "技术部",
    "skill_id": "skill_rigorous"
  }'

# 绑定员工 Skill
curl -X POST http://localhost:8001/admin/employees/ou_xxxxxxxxxxxxx/bind-skill \
  -H "Content-Type: application/json" \
  -d '{"skill_id": "skill_efficient"}'
```

---

## 回答风格详解

### 严谨型（rigorous）
```
温度：0.3（低，答案确定性高）
最大 Token：3000

示例输出：
## RAG 技术工作原理

### 一、核心概念
RAG（Retrieval-Augmented Generation，检索增强生成）是一种结合了
信息检索与大模型生成的混合架构...

### 二、工作流程
1. **索引构建阶段**
   - 文档解析与清洗
   - 文本分块（Chunking）
   - 向量化嵌入（Embedding）
   - 存储至向量数据库

2. **查询回答阶段**
   - 用户问题向量化
   - 相似度检索（余弦相似度）
   - 重排序（Reranker）
   - 上下文增强生成

### 三、参考资料
[来源: RAG技术白皮书 v2.1]
```

### 高效型（efficient）
```
温度：0.5（中，有一定创造性）
最大 Token：1000

示例输出：
**RAG = 检索 + 生成**

核心框架：
  问题 → 向量化 → 语义检索 → 上下文拼接 → LLM 生成

关键节点：
  1. 向量化质量决定检索上限
  2. Reranker 决定上下文相关性
  3. Chunk 大小影响答案粒度

方向指引：
  - 想提升检索精度 → 看 Embedding 模型选型
  - 想提升生成质量 → 看 Prompt 工程
  - 想提升响应速度 → 看向量数据库性能
```

### 新人友好型（beginner）
```
温度：0.8（较高，回答更口语化）
最大 Token：2000

示例输出：
## RAG 是什么？

想象一下，你有一个超级聪明的图书馆管理员 📚

**没有 RAG 的时候：**
这个管理员（就像 ChatGPT）只记得他上学时学过的东西，
如果问他最新的技术，他可能会"胡编乱造"（这叫"幻觉"）...

**有了 RAG 之后：**
管理员多了一个超级能力——可以实时查资料！
当你问他问题时，他会先快速翻阅公司资料库，
找到相关内容后，结合这些资料来回答你。

**打个比方 👇**
RAG 就像给一个聪明的学生配备了参考书。
考试时不是死记硬背，而是边查书边答题，
既保证了准确性，又保证了时效性！

**具体怎么做呢？**
1️⃣ 先把公司资料整理好，分成一小段一小段（这叫"分块"）
2️⃣ 把每段内容变成数字（这叫"向量化"），这样电脑才能理解语义
3️⃣ 用户提问时，也把问题变成数字，在资料库中找"意思最像"的段落
4️⃣ 把找到的段落和问题一起喂给 AI，让 AI 参考着回答
```

---

## 管理后台使用

启动管理后台：
```bash
python main.py --feishu-admin
```

访问地址：`http://localhost:8502`

功能模块：
- **状态总览**：查看 API 连接状态、飞书 Bot 状态、配置检查
- **Skill 管理**：创建、编辑、删除 Skill 模板
- **员工管理**：查看员工列表、绑定 Skill、注册新员工
- **风格预览**：预览不同 Skill 对同一问题的回答风格
- **会话记录**：查看员工与 Bot 的对话历史
- **配置指南**：飞书应用创建步骤参考

---

## API 接口一览

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/feishu/webhook` | 飞书 URL 验证 |
| `POST` | `/feishu/webhook` | 飞书事件回调 |
| `GET` | `/feishu/health` | 飞书 Bot 健康检查 |
| `GET` | `/admin/skills` | 获取所有 Skill |
| `POST` | `/admin/skills` | 创建 Skill |
| `PUT` | `/admin/skills/{id}` | 更新 Skill |
| `DELETE` | `/admin/skills/{id}` | 删除 Skill |
| `GET` | `/admin/employees` | 获取所有员工 |
| `POST` | `/admin/employees` | 注册员工 |
| `POST` | `/admin/employees/{feishu_user_id}/bind-skill` | 绑定员工 Skill |
| `GET` | `/admin/feishu/sessions` | 获取飞书会话列表 |

---

## 数据模型

```
┌──────────────────┐     ┌──────────────────────┐
│  EmployeeModel   │     │  SkillTemplateModel   │
├──────────────────┤     ├──────────────────────┤
│ id               │◄────│ skill_id             │
│ feishu_user_id   │     │ name                 │
│ name             │     │ answer_style         │
│ department       │     │ temperature          │
│ skill_id ─────────┼────►│ max_tokens           │
│ is_active        │     │ system_prompt_suffix │
└──────────────────┘     │ knowledge_scope      │
         │               └──────────────────────┘
         ▼
┌──────────────────┐
│ FeishuSessionModel│
├──────────────────┤
│ id               │
│ feishu_user_id   │
│ feishu_chat_id   │
│ employee_id      │
│ message_count    │
└──────────────────┘
```

---

## 常见问题

### Q: 飞书消息接收不到？
检查：
1. 飞书应用是否已发布/启用
2. 事件订阅的 URL 是否公网可访问
3. 是否订阅了 `im.message.receive_v1` 事件
4. `.env` 中的 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 是否正确

### Q: 员工首次发消息没有响应？
系统会自动注册员工。如果仍无响应，检查：
1. Bot 是否已添加到群组或开启了单聊
2. 消息类型是否为 text（非 text 类型会被忽略）

### Q: 如何更换员工的 Skill？
两种方式：
1. 管理后台：员工管理 → 选择员工 → 绑定 Skill
2. API：`POST /admin/employees/{feishu_user_id}/bind-skill`

### Q: 支持流式回复吗？
当前版本支持配置 `FEISHU_ENABLE_STREAMING=true`，但飞书卡片消息不支持流式更新，
建议保持默认关闭，使用普通卡片消息回复。

### Q: 本地开发如何测试？
使用 ngrok 等内网穿透工具：
```bash
ngrok http 8001
# 将返回的公网 URL 填入飞书事件订阅
# 例如：https://xxxx.ngrok-free.app/feishu/webhook
```
