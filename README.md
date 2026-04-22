"""
# 本地 RAG Demo 使用指南

## 功能特性

- 📄 **多格式文档支持**: PDF、Word、Excel、PPT、TXT、Markdown、JSON、YAML、HTML 等
- 🔍 **多格式差异化清洗**: PDF / TXT / Excel / Word 各自采用独立清洗策略
- 🏷️ **PDF 三分类智能识别**: 营销白皮书 / 网页导出型 / 社区引流型，自动适配清洗逻辑
- 🏷️ **自动标签提取**: 分片时自动打标签（运维/部署/产品等），查询时匹配标签精排召回
- 🏷️ **个性化回答**: 根据匹配的文档标签动态调整回答风格和侧重点
- 🔍 **父子文档分片**: 保证语义完整性，支持上下文关联
- 🏆 **向量检索 + Reranker**: 先粗排后精排，提高检索精度
- 💬 **上下文记忆**: 多轮对话，保留历史上下文
- 🌐 **外部大模型**: 知识库无答案时自动调用公网 LLM
- 📚 **文档管理**: 上传、查看、搜索、删除文档
- 📊 **会话管理**: 创建、切换、删除历史会话

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Ollama

确保 Ollama 服务已启动，并拉取所需模型：

```bash
# 启动 Ollama 服务
ollama serve

# 拉取 Embedding 模型
ollama pull bge-m3

# 拉取生成模型
ollama pull qwen3:8b
```

### 3. 启动服务

方式一：使用 Python 启动

```bash
# 启动 API 后端（终端 1）
python main.py --api

# 启动 Web UI（终端 2）
python main.py --ui
```

方式二：直接启动

```bash
# API 后端
python -m uvicorn api.server:app --host 0.0.0.0 --port 8001

# Web UI（另一个终端）
streamlit run web_app/app.py --server.port 8501
```

### 4. 访问界面

打开浏览器访问: http://localhost:8501

## 使用流程

### 4.1 上传文档

1. 点击「文档管理」标签页
2. 选择文件上传或输入目录路径
3. 等待处理完成

### 4.2 提问

1. 点击「问答」标签页
2. 输入问题并点击发送
3. 查看回答和参考来源

### 4.3 查看历史

1. 在左侧边栏查看历史会话
2. 点击会话可切换
3. 删除不需要的会话

## API 接口

### 查询

```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "你的问题"}'
```

### 上传文档

```bash
curl -X POST http://localhost:8001/upload/document \
  -F "file=@文档路径"
```

### 搜索

```bash
curl "http://localhost:8001/search?query=关键词&top_k=10"
```

## 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并修改：

```bash
cp .env.example .env
```

### 主要配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| OLLAMA_BASE_URL | Ollama 服务地址 | http://localhost:11434 |
| OLLAMA_MODEL | 生成模型 | qwen3:8b |
| OLLAMA_EMBED_MODEL | Embedding 模型 | bge-m3 |
| VECTOR_DB_TYPE | 向量数据库类型 | qdrant |
| TOP_K | 粗排召回数量 | 20 |
| RERANK_TOP_K | 精排返回数量 | 10 |
| RERANK_THRESHOLD | 重排得分阈值 | 0.5 |

### 切换向量数据库

1. **Qdrant** (推荐):
```python
VECTOR_DB_TYPE=qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

2. **ChromaDB** (轻量):
```python
VECTOR_DB_TYPE=chroma
```

3. **本地文件** (开发测试):
```python
VECTOR_DB_TYPE=file
```

### 外部大模型

1. **OpenAI**:
```python
EXTERNAL_LLM_PROVIDER=openai
EXTERNAL_LLM_API_KEY=sk-xxx
EXTERNAL_LLM_MODEL=gpt-4o-mini
```

2. **Claude**:
```python
EXTERNAL_LLM_PROVIDER=claude
EXTERNAL_LLM_API_KEY=sk-ant-xxx
EXTERNAL_LLM_MODEL=claude-3-5-haiku-20241022
```

3. **通义千问**:
```python
EXTERNAL_LLM_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-xxx
```

## 多格式差异化清洗

### TXT 清洗规则

- 提取并规范化头部元数据（标题、作者、日期、版本等）
- 删除重复段落（出现 3 次以上的段落自动过滤）
- 删除口语化引导语（"大家好"、"首先"、"OK" 等）
- 清理格式噪声（多余分隔符、空引用行）

### PDF 三分类 + 差异化清洗

| 类型 | 特征 | 清洗策略 |
|------|------|----------|
| **营销白皮书** | 多栏排版、章节符号【】、多级编号 | 线性重组与语境缝合：拼接孤立短行，恢复文档结构层级 |
| **网页导出型** | URL、单栏、导航版权信息 | 断句连贯与外围去噪：修复意外截断句子，去除页眉页脚和导航元素 |
| **社区引流型** | 干货技术词 + 广告引流词并存 | 业务截断与实体格式化：在引流点前截断，技术实体（代码/命令/版本号）规范化保留 |

PDF 类型自动检测，通过文本特征（URL 密度、多级编号、引流关键词）综合评分判断，无需手动指定。

### Excel / Word 清洗规则

- 保留表格结构（统一使用 `|` 分隔符）
- 清理格式符号（多余括号、首尾分隔符）
- 清理单元格内多余空格
- 规范化行内空白

## 文档分片策略

### 三种文档类型 + 最优分片策略

| 文档类型 | 检测特征 | 分片策略 | 设计原则 |
|----------|---------|---------|---------|
| **article** | Markdown 标题 `# ## ###` ≥2 | Markdown 标题 + 段落分片 | 保留层级结构，按章节边界切分 |
| **spreadsheet** | `|` 分隔行占比 >20% | 表格结构分片 | 不破坏行列结构，保留表头上下文 |
| **notes** | 短段落 + 标题关键词 | 自然段落分片 | 保留语义连贯性，不过度切割 |

### 自动标签提取

每个分片在创建时自动提取主题标签（最多 5 个）：

| 标签 | 触发关键词 |
|------|-----------|
| 运维 | 监控、部署、上线、Docker、K8s、Jenkins、日志、告警 |
| 部署 | 集群、节点、副本、环境、Docker 镜像、Helm、Ingress |
| 产品 | 功能、特性、规格、型号、版本、发布说明、定价 |
| 开发 | 代码、API、SDK、Git、CI/CD、框架、算法 |
| 安全 | 加密、认证、鉴权、权限、WAF、漏洞 |
| 数据库 | MySQL、Redis、索引、事务、慢查询、分库分表 |
| 网络 | TCP、HTTP、负载均衡、网关、CDN、VPC |
| 云服务 | AWS、阿里云、ECS、S3、Serverless、容器服务 |
| AI | LLM、Embedding、RAG、知识库、Prompt、微调 |
| 财务 | 账单、计费、成本、预算、发票、报价 |
| 支持 | 工单、故障申报、服务台、SLA、响应时间 |

### 个性化召回与回答

1. **查询关键字提取** — 从用户问题中提取关键词和匹配的领域标签
2. **Tag-Boosted 重排** — Reranker 分数 + 关键字/标签匹配分数加权，优先召回领域匹配的片段
3. **个性化提示词** — 根据匹配的标签动态调整回答风格（运维重步骤、开发重原理、产品重规格等）

### 父子文档架构

所有分片类型均保留父子文档双层结构：

- **父文档**：包含完整上下文，合并多个子块，检索时用于去重和提供完整背景
- **子文档**：语义完整的最小单元，检索和 Reranker 的实际处理对象
- 子文档通过 `parent_id` 引用父文档，形成完整的上下文链

## 目录结构

```
RAG_New/
├── api/              # FastAPI 后端
│   └── server.py     # API 服务
├── config/           # 配置
│   └── settings.py   # 配置管理
├── core/             # 核心模块
│   ├── chunker.py    # 父子文档分片
│   ├── embedding.py  # 向量化（支持 Ollama / OpenAI / DashScope）
│   ├── reranker.py   # 重排序
│   ├── rag_engine.py # RAG 引擎
│   └── history_manager.py  # 历史管理
├── llm/              # 大模型接口
│   └── llm_client.py # 多模型支持（Ollama / OpenAI / Claude / DashScope）
├── parsers/          # 文档解析
│   ├── document_parser.py  # 多格式解析（含 PDF 元数据提取）
│   └── data_cleaner.py     # 多格式差异化清洗（PDF 三分类 / TXT / Excel / Word）
├── storage/          # 文档存储
│   └── document_storage.py # 文档管理
├── vectorstore/      # 向量存储
│   └── vector_store.py     # Qdrant / Chroma / 本地文件
├── web_app/          # Streamlit UI
│   └── app.py        # Web 界面
├── data/             # 数据目录
│   ├── documents/    # 原始文档
│   ├── cleaned/      # 清洗后文档
│   ├── vectors/      # 向量数据
│   └── sessions.json # 会话历史
├── main.py           # 主入口
├── requirements.txt  # 依赖
└── .env.example      # 环境变量示例
```

## 常见问题

### Q: Ollama 连接失败

确保 Ollama 服务已启动：
```bash
ollama serve
```

### Q: 文档上传失败

检查文件格式是否支持，大小是否超过限制（默认 50MB）。

### Q: 检索结果为空

确认文档已成功处理并索引。检查状态是否为 "indexed"。

### Q: 回答质量差

1. 尝试调整 `RERANK_THRESHOLD`（降低阈值可召回更多）
2. 确认 Embedding 模型与文档语言匹配
3. 检查文档内容质量

## 开发

### 运行测试

```bash
pytest tests/
```

### 代码结构

核心流程：
1. `parsers/document_parser.py` - 多格式文档解析，提取文本和元数据
2. `parsers/data_cleaner.py` - 多格式差异化清洗（PDF 三分类 / TXT / Excel / Word）
3. `core/chunker.py` - 文档类型检测 + 三种分片策略 + 自动标签提取 + 父子文档分片
4. `core/embedding.py` - 向量化（支持 Ollama / OpenAI / DashScope）
5. `core/reranker.py` - 重排序
6. `vectorstore/` - 向量存储（Qdrant / Chroma / 本地文件）
7. `core/rag_engine.py` - RAG 引擎（含 Tag-Boosted 重排 + 个性化提示词）
8. `llm/llm_client.py` - 大模型接口（Ollama / OpenAI / Claude / DashScope）
9. `api/` / `web_app/` - 服务接口
"""
