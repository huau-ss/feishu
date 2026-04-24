# 本地 RAG 知识库问答系统

基于 FastAPI + 飞书机器人 + RAG 的本地知识库问答系统，支持共享知识库、个人笔记（赛博员工）和公网大模型融合检索。

---

## 系统架构

```
用户提问 (飞书 / Web UI)
       │
       ▼
┌─────────────────────┐
│  FeishuBot / Web API │
└──────────┬──────────┘
           │
           ▼
  ┌────────────────────┐
  │  _query_with_skill │
  └────────┬───────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  共享知识库    个人知识库
  (Vector DB)   (赛博员工)
     │           │
     └─────┬─────┘
           │ 两者都有内容?
       ┌───┴───────────────────────┐
       │ Yes                       │ No
       ▼                           ▼
  本地 LLM                    公网 LLM 兜底
  (海纳一体机)               (DeepSeek / OpenAI / Claude)
       │                           │
       └───────────┬───────────────┘
                   ▼
            返回答案 + 来源
```

---

## 查询流程

1. **共享知识库检索** — 从向量数据库（Qdrant）中检索相关文档块
2. **个人知识库检索** — 从个人笔记、知识图谱、记忆中检索
3. **决策判断**
   - 知识库有结果（共享KB **或** 个人KB） → 本地 LLM 基于上下文生成答案
   - 知识库都没有结果 → 公网大模型兜底，生成独立回答
4. **赛博员工学习** — 从对话中提取用户偏好，更新个人记忆和知识图谱

---

## 支持的文件格式

系统支持以下文件格式的解析、清洗与向量化：

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | `.pdf` | PyMuPDF 文本提取，支持白皮书/网页导出/社区引流三分类清洗 |
| Word | `.docx`, `.doc` | python-docx 解析段落和表格 |
| Excel | `.xlsx`, `.xls` | openpyxl 按工作表解析 |
| PowerPoint | `.pptx`, `.ppt` | python-pptx 按幻灯片解析 |
| HTML | `.html`, `.htm` | BeautifulSoup 提取正文，移除脚本样式 |
| 纯文本 | `.txt`, `.md`, `.json`, `.yaml`, `.yml`, `.cfg`, `.conf`, `.log` | 多编码自动识别 |
| 邮件 | `.eml`, `.msg` | 提取主题、发件人、收件人和正文 |
| **XML** | `.xml` | XML 标签结构解析，提取元素文本和属性 |
| **ZIP** | `.zip` | 解压并递归解析内部文本/代码/表格文件 |
| **CSV** | `.csv` | 表格解析，自动识别分隔符并转为 Markdown 表格 |
| **RTF** | `.rtf` | 富文本格式解析，移除格式控制符 |
| **视频/音频** | `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`, `.webm`, `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` | FFmpeg 提取音频 + Whisper 语音转文字 |

> **视频/音频处理说明**：需安装 FFmpeg（[下载](https://ffmpeg.org/download.html)）和 `faster-whisper`（`pip install faster-whisper`）。支持中英文自动识别，按时间戳分段输出转写文本。

**清洗后文档格式**：所有文件清洗后均以 Markdown 格式保存至 `data/cleaned/` 目录，包含 YAML frontmatter 元数据、基本信息表格、标签及正文。

---

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量（可选，推荐）

在项目根目录创建 `.env` 文件：

```bash
# .env 示例
MYSQL_PASSWORD=your_mysql_password
EXTERNAL_LLM_API_KEY=your_api_key
FEISHU_APP_SECRET=your_feishu_secret
```

> `.env` 中的值会覆盖 `settings.py` 中的默认值。

### 3. 启动服务

```bash
# 方式一：只启动 API 后端（推荐用于飞书机器人）
python main.py --api

# 方式二：启动 API + Web UI（Streamlit）
python main.py

# 方式三：只启动 Web UI
python main.py --ui

# 方式四：快速演示模式
python main.py --demo
```

默认端口：
- API: `http://localhost:8001`
- Web UI: `http://localhost:8501`

---

## 配置说明

所有配置项集中在 `config/settings.py`，可通过环境变量或 `.env` 文件覆盖。

### 数据库

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `MYSQL_HOST` | `localhost` | MySQL 主机 |
| `MYSQL_PORT` | `3306` | MySQL 端口 |
| `MYSQL_USER` | `root` | MySQL 用户名 |
| `MYSQL_PASSWORD` | `123456` | MySQL 密码 |
| `MYSQL_DATABASE` | `rag_knowledge_base` | 数据库名 |

> 首次启动会自动创建所需的表。

### 本地 LLM（Ollama）

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `OLLAMA_BASE_URL` | `http://localhost:8000` | Ollama 服务地址 |
| `OLLAMA_MODEL` | `qwen3-vl:4b` | 生成模型名称 |
| `OLLAMA_EMBED_MODEL` | `bge-m3` | Embedding 模型名称 |

> 仅在未配置海纳数聚一体机时使用。

### 海纳数聚 AI 一体机（推荐）

本地部署的一体机提供 LLM、Embedding 和 Reranker 服务。

**大语言模型：**

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `HAINAN_LLM_BASE_URL` | `http://192.168.3.86:18051/v1` | LLM API 地址 |
| `HAINAN_LLM_MODEL` | `qwen3_30b_a3b` | 模型名称 |
| `HAINAN_LLM_API_KEY` | `""` | API Key（通常留空） |

**向量嵌入模型：**

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `HAINAN_EMBED_BASE_URL` | `http://192.168.3.86:6208/v1` | Embedding API 地址 |
| `HAINAN_EMBED_MODEL` | `bce-embedding-base_v1` | Embedding 模型 |
| `HAINAN_EMBED_DIM` | `1536` | 向量维度 |
| `HAINAN_EMBED_API_KEY` | `""` | API Key（通常留空） |

**重排模型：**

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `HAINAN_RERANK_BASE_URL` | `http://192.168.3.86:6006/v1` | Reranker API 地址 |
| `HAINAN_RERANK_MODEL` | `bce-reranker-base_v1` | Reranker 模型 |
| `HAINAN_RERANK_API_KEY` | `""` | API Key（通常留空） |

### 公网大模型（兜底）

当本地知识库和个人笔记都没有相关内容时，系统自动调用公网大模型。

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `EXTERNAL_LLM_PROVIDER` | `openai` | 提供商：`openai` / `claude` / `dashscope` / `deepseek` |
| `EXTERNAL_LLM_API_KEY` | `sk-f5e83e1f...` | API Key |
| `EXTERNAL_LLM_BASE_URL` | `https://api.deepseek.com/v1` | API 地址 |
| `EXTERNAL_LLM_MODEL` | `deepseek-chat` | 模型名称 |

> 内部使用 OpenAI 兼容格式。DeepSeek、硅基流动、阿里云等 OpenAI 兼容接口均可使用。

### RAG 参数

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `VECTOR_DIM` | `768` | 向量维度（与 Embedding 模型匹配） |
| `TOP_K` | `20` | 粗排阶段召回的文档块数量 |
| `RERANK_TOP_K` | `10` | 精排后返回的文档块数量 |
| `RERANK_THRESHOLD` | `0.5` | 重排得分阈值，低于此值的块被过滤 |
| `MAX_CONTEXT_CHUNKS` | `3` | 最终送入 LLM 的最多块数 |

> `RERANK_THRESHOLD` 可调高以减少幻觉（更严格依赖知识库），调低以增加回答覆盖率。

### 文档处理

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `CHUNK_SIZE` | `800` | 子文档块大小（字符） |
| `CHUNK_OVERLAP` | `100` | 子文档块重叠大小 |
| `PARENT_CHUNK_SIZE` | `2000` | 父文档块大小（用于检索去重） |
| `MAX_FILE_SIZE` | `50MB` | 最大上传文件大小 |

### 向量数据库

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `VECTOR_DB_TYPE` | `qdrant` | 向量数据库类型：`qdrant` / `chroma` |
| `QDRANT_HOST` | `localhost` | Qdrant 主机 |
| `QDRANT_PORT` | `6333` | Qdrant HTTP 端口 |
| `QDRANT_COLLECTION` | `knowledge_base` | 集合名称 |

### 服务器

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `API_HOST` | `0.0.0.0` | API 监听地址 |
| `API_PORT` | `8001` | API 端口 |
| `STREAMLIT_PORT` | `8501` | Web UI 端口 |

### 飞书 Bot

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `FEISHU_APP_ID` | `cli_a96db55728e45cc4` | 飞书应用 App ID |
| `FEISHU_APP_SECRET` | `DNfJyNRIDPyUj...` | 飞书应用 App Secret |
| `FEISHU_VERIFICATION_TOKEN` | `""` | 飞书事件验证 Token |
| `FEISHU_WEBHOOK_PATH` | `/feishu/webhook` | Webhook 路径 |
| `FEISHU_ENABLE_STREAMING` | `False` | 是否启用流式回复 |
| `FEISHU_RATE_LIMIT_PER_MINUTE` | `20` | 每分钟最大请求数 |

---

## 飞书机器人命令

发送以下命令给机器人：

| 命令 | 说明 |
|------|------|
| `开启赛博员工` / `启用个人知识库` | 启用个人知识库功能 |
| `关闭赛博员工` / `禁用个人知识库` | 关闭个人知识库功能 |
| `创建笔记`<br>标题: xxx<br>内容: xxx<br>标签: xxx, xxx | 新建笔记 |
| `查看笔记` / `我的笔记` | 查看笔记列表 |
| `搜索笔记 + 关键词` | 搜索笔记 |
| `删除笔记 + 标题` | 删除笔记 |
| `我的知识图谱` | 查看知识图谱 |
| `我的记忆` | 查看个人记忆 |
| `帮助` / `help` | 查看所有命令 |

---

## 目录结构

```
RAG-main/
├── config/
│   └── settings.py       # 所有配置项
├── core/
│   ├── rag_engine.py     # RAG 核心引擎
│   ├── chunker.py        # 文档分块策略
│   ├── embedding.py      # 向量嵌入模型
│   ├── reranker.py       # 重排模型
│   ├── personal_knowledge.py   # 个人知识库
│   ├── personal_rag.py   # 个性化 RAG（赛博员工）
│   └── skill_templates.py # Skill 个性化模板
├── database/
│   └── models.py         # SQLAlchemy 模型
├── feishu/
│   ├── bot.py            # 飞书 Bot 核心逻辑
│   ├── webhook.py        # 飞书 Webhook 路由
│   ├── client.py         # 飞书 API 客户端
│   └── employee_manager.py # 员工与 Skill 管理
├── llm/
│   └── llm_client.py     # LLM 客户端（Ollama/OpenAI/Claude/DashScope）
├── parsers/
│   ├── document_parser.py  # 文档解析器（PDF/Word/Excel/PPT/HTML/XML/ZIP/CSV/RTF/视频）
│   └── data_cleaner.py     # 数据清洗模块（格式差异化清洗）
├── storage/
│   └── document_storage.py # 文档元数据存储
├── vectorstore/
│   └── vector_store.py   # 向量数据库接口
├── api/
│   └── server.py         # FastAPI 服务入口
├── web_app/
│   └── app.py            # Streamlit Web UI
└── main.py               # 统一入口脚本
```

---

## 常见问题

### Q: 公网大模型没有调用？

1. 检查 `EXTERNAL_LLM_API_KEY` 是否配置了正确的 API Key
2. 检查 `EXTERNAL_LLM_BASE_URL` 和 `EXTERNAL_LLM_MODEL` 是否正确
3. 确认海纳数聚一体机的 `HAINAN_LLM_BASE_URL` 未被误填（会优先于公网 LLM 作为本地 LLM 使用，但不影响公网兜底）
4. 重启 FastAPI 服务使配置生效

### Q: 知识库检索没有结果？

1. 确认文档已上传并成功索引（`POST /documents` 查看状态）
2. 检查向量数据库（Qdrant）是否正常运行
3. 检查 Embedding 模型是否可用

### Q: 飞书机器人无响应？

1. 确认飞书 Webhook URL 已正确配置在飞书开放平台
2. 确认飞书应用已启用机器人功能
3. 检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 是否正确
4. 查看服务端日志中的 `feishu.bot` 相关输出

### Q: 视频/音频文件无法处理？

1. 确认已安装 FFmpeg 并添加到系统 PATH（终端运行 `ffmpeg -version` 验证）
2. 确认已安装 `faster-whisper`（`pip install faster-whisper`）
3. 检查文件大小是否超过 `MAX_FILE_SIZE` 限制
4. 确认文件格式受支持（MP4/AVI/MOV/MKV/FLV/WMV/WebM/MP3/WAV/M4A/FLAC/OGG）

### Q: ZIP 文件解压后部分文件未解析？

1. ZIP 内只有文本类文件（TXT/MD/JSON/XML/HTML）会被直接解析
2. 二进制文件（PDF/DOCX/XLSX/PPTX/RTF）需要通过单独上传处理
3. 压缩包内代码文件（PY/JS/JAVA/GO/RS/SH/SQL）会截取前 50 行作为摘要
