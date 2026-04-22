"""
文档分片模块
支持按文档类型选择最优分片策略，同时保留父子文档分片架构：
- article: Markdown 标题 + 段落分片（保留层级结构）
- spreadsheet: 表格结构分片（按行切分，保留表头上下文）
- notes: 自然段落分片（检测标题关键词）
父子文档分片保证语义完整性和上下文关联。
"""
import uuid
import logging
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# 文档类型枚举
# ============================================================================

class DocType(Enum):
    """文档类型"""
    ARTICLE = "article"           # 文章（Markdown / 长段落 / 多级标题）
    SPREADSHEET = "spreadsheet"   # 表格（Excel / CSV / 行列结构）
    NOTES = "notes"              # 笔记（自然段落 / 标题关键词）
    CONFIG = "config"            # 配置（键值对 / 结构化）
    UNKNOWN = "unknown"


# ============================================================================
# 数据类
# ============================================================================

@dataclass
class TextChunk:
    """文本块"""
    chunk_id: str                          # 块 ID
    content: str                            # 块内容
    chunk_index: int                        # 块索引
    parent_id: Optional[str] = None         # 父文档 ID
    is_parent: bool = False                 # 是否为父文档
    metadata: Dict = field(default_factory=dict)   # 元数据（含 tags）


@dataclass
class ChunkingResult:
    """分片结果"""
    doc_id: str                             # 文档 ID
    doc_type: DocType                       # 文档类型
    parent_chunks: List[TextChunk] = field(default_factory=list)   # 父文档块
    child_chunks: List[TextChunk] = field(default_factory=list)   # 子文档块
    total_chars: int = 0                    # 总字符数


# ============================================================================
# 自动标签提取器
# ============================================================================

class AutoTagger:
    """
    从文档内容中自动提取主题标签

    策略：
    - 基于关键词匹配提取领域标签
    - 基于文档标题/结构推断标签
    - 基于段落高频词提取标签
    """

    # 领域关键词 → 标签映射
    DOMAIN_KEYWORDS: Dict[str, List[str]] = {
        "运维": [
            "运维", "监控", "部署", "上线", "发布", "回滚", "迁移",
            "nginx", "docker", "k8s", "kubernetes", "ansible",
            "jenkins", "cicd", "shell", "prometheus", "grafana",
            "日志", "告警", "故障", "容灾", "备份", "恢复",
        ],
        "开发": [
            "开发", "编程", "代码", "接口", "api", "sdk",
            "前端", "后端", "全栈", "调试", "测试", "debug",
            "git", "github", "ci/cd", "单元测试", "集成测试",
            "框架", "库", "模块", "函数", "类", "算法",
        ],
        "部署": [
            "部署", "安装", "配置", "集群", "节点", "副本",
            "环境", "开发环境", "测试环境", "生产环境", "预发布",
            "docker", "镜像", "容器", "编排", "yaml", "helm",
            "ingress", "service", "pod", "deployment",
        ],
        "安全": [
            "安全", "加密", "解密", "认证", "授权", "鉴权",
            "防火墙", "渗透", "漏洞", "waf", "ddos", "xss",
            "sql注入", "权限", "角色", "oauth", "jwt", "token",
        ],
        "产品": [
            "产品", "功能", "特性", "规格", "参数", "型号",
            "版本", "发布说明", "roadmap", "需求", "竞品",
            "用户", "客户", "市场", "定价", "套餐",
        ],
        "数据库": [
            "数据库", "db", "sql", "mysql", "postgresql", "redis",
            "表", "索引", "主键", "外键", "事务", "锁",
            "查询", "优化", "慢查询", "分库分表", "读写分离",
        ],
        "网络": [
            "网络", "tcp", "udp", "http", "https", "dns", "cdn",
            "负载均衡", "网关", "路由", "交换机", "路由器",
            "vpc", "子网", "ip", "端口", "协议", "带宽",
        ],
        "云服务": [
            "云", "aws", "azure", "gcp", "aliyun", "阿里云", "腾讯云",
            "ecs", "s3", "lambda", "serverless", "容器服务",
            "对象存储", "cdn", "vpc", "ecs", "rds",
        ],
        "AI": [
            "ai", "llm", "大模型", "gpt", "embedding", "向量",
            "rag", "rag", "知识库", "检索", "训练", "微调",
            "prompt", "幻觉", "token", "推理", "agent",
        ],
        "财务": [
            "财务", "账单", "计费", "费用", "成本", "预算",
            "发票", "报销", "采购", "合同", "价格", "报价",
            "人民币", "美元", "结算", "对账", "月结",
        ],
        "行政": [
            "行政", "办公", "会议室", "出差", "请假", "考勤",
            "招聘", "入职", "离职", "合同", "绩效", "培训",
        ],
        "技术支持": [
            "技术支持", "客服", "工单", "问题", "故障申报",
            "服务台", "helpdesk", "sla", "响应时间", "解决率",
        ],
    }

    # 黑名单词：太泛化，不适合作为标签
    BLACKLIST = {
        "我们", "你", "他", "这个", "那个", "的", "了", "是",
        "公司", "部门", "项目", "任务", "内容", "文档", "文件",
        "相关", "以上", "以下", "包括", "包含", "以及", "或者",
        "请", "请勿", "注意", "说明", "描述", "情况", "问题",
        "方法", "方式", "情况", "原因", "结果", "作用", "效果",
    }

    @classmethod
    def extract_tags(cls, text: str, title: str = "", max_tags: int = 5) -> List[str]:
        """
        从文档中提取标签

        Args:
            text: 文档内容
            title: 文档标题
            max_tags: 最大标签数量

        Returns:
            标签列表（如 ["运维", "部署", "产品"]）
        """
        text_lower = text.lower()
        title_lower = title.lower()
        combined = f"{title_lower} {text_lower}"

        # 统计每个领域匹配的关键词数量
        domain_scores: Dict[str, int] = {}
        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            score = 0
            for kw in keywords:
                # 标题中出现关键词权重更高
                if kw.lower() in title_lower:
                    score += 3
                # 计算出现次数（避免标题权重过高导致其他标签被忽略）
                count = combined.lower().count(kw.lower())
                score += min(count, 3)  # 最多计3次
            if score > 0:
                domain_scores[domain] = score

        if not domain_scores:
            return []

        # 按分数排序，取 top N
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        tags = [domain for domain, score in sorted_domains[:max_tags]]

        logger.debug(f"Auto-tagged: {tags} (scores: {dict(sorted_domains[:max_tags])})")
        return tags

    @classmethod
    def extract_keywords_from_query(cls, query: str, max_keywords: int = 5) -> List[str]:
        """
        从用户查询中提取关键词（用于匹配标签）

        Args:
            query: 用户问题
            max_keywords: 最大关键词数量

        Returns:
            关键词列表
        """
        # 停用词
        stopwords = {
            "的", "了", "是", "在", "和", "与", "或", "及", "等",
            "请问", "怎么", "如何", "什么", "哪些", "有没有",
            "能", "可以", "请", "一下", "帮助", "告诉",
            "我", "你", "他", "她", "它", "们",
            "这", "那", "这个", "那个", "这些", "那些",
        }

        # 提取中文词
        words = re.findall(r'[\u4e00-\u9fa5]{2,}', query)
        # 提取英文词
        words += re.findall(r'[a-zA-Z]{2,}', query.lower())

        # 过滤停用词和太短的词
        filtered = [w for w in words if w not in stopwords and len(w) >= 2]

        # 统计词频
        from collections import Counter
        word_counts = Counter(filtered)

        # 取高频词
        top_words = [w for w, _ in word_counts.most_common(max_keywords)]

        # 尝试匹配领域标签
        query_lower = query.lower()
        matched_tags = []
        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in query_lower:
                    if domain not in matched_tags:
                        matched_tags.append(domain)
                    break

        # 返回：领域标签优先，其次高频词
        result = matched_tags + [w for w in top_words if w not in matched_tags]
        return result[:max_keywords]


# ============================================================================
# 分片策略基类
# ============================================================================

class ChunkingStrategy:
    """分片策略基类"""

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        parent_chunk_size: int = 2000,
        min_chunk_size: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.parent_chunk_size = parent_chunk_size
        self.min_chunk_size = min_chunk_size

    def split(
        self,
        text: str,
        doc_id: str,
        metadata: Dict,
    ) -> Tuple[List[str], List[Dict]]:
        """
        执行分片

        Args:
            text: 待分片文本
            doc_id: 文档 ID
            metadata: 元数据

        Returns:
            (文本块列表, 块元数据列表)
        """
        raise NotImplementedError

    def _normalize_whitespace(self, text: str) -> str:
        """规范化空白"""
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text


# ============================================================================
# 策略一: Article 分片（Markdown 标题 + 段落）
# ============================================================================

class ArticleChunkingStrategy(ChunkingStrategy):
    """
    文章类分片策略

    设计原则：按章节层级切分，保留 Markdown 标题结构

    规则：
    - 识别 Markdown 标题层级（# ## ###）
    - 标题作为章节分界点
    - 大章节内部按段落累积，超过阈值后切分
    - 保留标题作为上下文前缀
    """

    # Markdown 标题正则
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    # 代码块（不切割）
    CODE_BLOCK_PATTERN = re.compile(r'```[\s\S]*?```', re.MULTILINE)

    def split(
        self,
        text: str,
        doc_id: str,
        metadata: Dict,
    ) -> Tuple[List[str], List[Dict]]:
        text = self._normalize_whitespace(text)

        # 临时替换代码块，避免标题识别错误
        code_blocks: List[str] = []
        def replace_code(m):
            code_blocks.append(m.group(0))
            return f"__CODE_BLOCK_{len(code_blocks)-1}__"

        text = self.CODE_BLOCK_PATTERN.sub(replace_code, text)

        # 收集所有标题和对应的段落
        sections: List[Tuple[Optional[str], str]] = []
        matches = list(self.HEADING_PATTERN.finditer(text))

        if not matches:
            # 无标题，降级为纯段落分片
            return self._split_by_paragraphs(text, doc_id, metadata)

        for i, m in enumerate(matches):
            heading_level = len(m.group(1))
            heading_text = m.group(2).strip()
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

            content = text[start:end].strip()
            # 还原代码块
            for j, cb in enumerate(code_blocks):
                content = content.replace(f"__CODE_BLOCK_{j}__", cb)

            sections.append((heading_text, content))

        # 还原剩余代码块
        sections_text = '\n\n'.join(
            f"## {h}\n{c}" if h else c for h, c in sections
        )
        for j, cb in enumerate(code_blocks):
            sections_text = sections_text.replace(f"__CODE_BLOCK_{j}__", cb)

        # 按段落累积，遇到标题重置
        chunks: List[str] = []
        chunk_metas: List[Dict] = []
        current_headings: List[str] = []
        current_lines: List[str] = []
        current_size = 0

        lines = sections_text.split('\n')
        for line in lines:
            is_heading = self.HEADING_PATTERN.match(line.strip())

            if is_heading:
                # 遇到新标题，先输出当前块
                if current_size >= self.min_chunk_size:
                    chunks.append('\n'.join(current_lines))
                    chunk_metas.append({
                        **metadata,
                        "section_headings": list(current_headings),
                        "chunk_type": "article",
                    })

                # 更新当前标题链
                level = len(is_heading.group(1))
                heading_text = is_heading.group(2).strip()
                # 移除高于当前层级的标题（向上合并）
                current_headings = [h for h in current_headings
                                   if h.startswith('#') and len(h) < level]
                current_headings.append(f"{'#' * level} {heading_text}")
                current_lines = [line]
                current_size = len(line)
            else:
                if current_size + len(line) > self.chunk_size and current_size >= self.min_chunk_size:
                    chunks.append('\n'.join(current_lines))
                    chunk_metas.append({
                        **metadata,
                        "section_headings": list(current_headings),
                        "chunk_type": "article",
                    })
                    # overlap
                    overlap_lines = current_lines[-(self.chunk_overlap // 30):]
                    current_lines = overlap_lines + [line]
                    current_size = sum(len(l) for l in current_lines)
                else:
                    current_lines.append(line)
                    current_size += len(line) + 1

        if current_size >= self.min_chunk_size:
            chunks.append('\n'.join(current_lines))
            chunk_metas.append({
                **metadata,
                "section_headings": list(current_headings),
                "chunk_type": "article",
            })

        return chunks, chunk_metas

    def _split_by_paragraphs(self, text: str, doc_id: str, metadata: Dict) -> Tuple[List[str], List[Dict]]:
        """无标题时降级为按段落分片"""
        chunks: List[str] = []
        chunk_metas: List[Dict] = []
        current_lines: List[str] = []
        current_size = 0

        for para in text.split('\n\n'):
            para = para.strip()
            if not para:
                continue

            if current_size + len(para) > self.chunk_size and current_size >= self.min_chunk_size:
                chunks.append('\n\n'.join(current_lines))
                chunk_metas.append({**metadata, "chunk_type": "article"})
                overlap = current_lines[-1:] if current_lines else []
                current_lines = overlap + [para]
                current_size = sum(len(l) for l in current_lines) + len(overlap)
            else:
                current_lines.append(para)
                current_size += len(para) + 2

        if current_size >= self.min_chunk_size:
            chunks.append('\n\n'.join(current_lines))
            chunk_metas.append({**metadata, "chunk_type": "article"})

        return chunks, chunk_metas


# ============================================================================
# 策略二: Spreadsheet 分片（保留表格结构）
# ============================================================================

class SpreadsheetChunkingStrategy(ChunkingStrategy):
    """
    表格类分片策略

    设计原则：不破坏行列结构，按行切分时保留表头上下文

    规则：
    - 识别表格行（| 分隔 或 \t 分隔）
    - 保留表头行作为每个块的前缀上下文
    - 按数据行累积，超过阈值后切分
    - 非表格段落单独处理
    """

    TABLE_ROW_PATTERN = re.compile(r'^\s*\|.+\|\s*$', re.MULTILINE)
    TAB_TABLE_PATTERN = re.compile(r'^\s*[^\|\n]+\t[^\|\n]+', re.MULTILINE)
    SEPARATOR_PATTERN = re.compile(r'^\s*\|[\s\-:]+\|\s*$')  # |---| 这样的分隔行

    def split(
        self,
        text: str,
        doc_id: str,
        metadata: Dict,
    ) -> Tuple[List[str], List[Dict]]:
        text = self._normalize_whitespace(text)

        lines = text.split('\n')
        chunks: List[str] = []
        chunk_metas: List[Dict] = []

        # 收集表头
        table_headers: List[str] = []
        current_table_rows: List[str] = []
        current_size = 0
        in_table = False

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            is_table_row = bool(self.TABLE_ROW_PATTERN.match(stripped))
            is_separator = bool(self.SEPARATOR_PATTERN.match(stripped))
            is_tab_table = bool(self.TAB_TABLE_PATTERN.match(stripped))

            if is_separator:
                continue  # 跳过表格分隔行

            if is_table_row or is_tab_table:
                # 标准化为 | 分隔
                row = stripped
                if is_tab_table:
                    row = ' | '.join(stripped.split('\t'))

                # 检测是否为表头（第一行或含有"名称/型号/规格"等）
                header_keywords = ['名称', '型号', '规格', '参数', '配置', '项目', 'name', 'model', 'spec', 'parameter']
                is_header = (
                    not table_headers
                    or any(kw in stripped.lower() for kw in header_keywords)
                )

                if is_header and not table_headers:
                    table_headers.append(row)
                    continue

                # 开始新的表格上下文
                if not in_table and current_size >= self.min_chunk_size and current_table_rows:
                    chunks.append('\n'.join([table_headers[-1]] + current_table_rows))
                    chunk_metas.append({
                        **metadata,
                        "table_headers": [table_headers[-1]],
                        "chunk_type": "spreadsheet",
                    })
                    current_table_rows = []
                    current_size = 0

                in_table = True
                current_table_rows.append(row)
                current_size += len(row) + 1

            else:
                # 非表格内容
                if in_table and current_table_rows:
                    # 输出当前表格块
                    chunks.append('\n'.join([table_headers[-1]] + current_table_rows))
                    chunk_metas.append({
                        **metadata,
                        "table_headers": [table_headers[-1]],
                        "chunk_type": "spreadsheet",
                    })
                    current_table_rows = []
                    current_size = 0
                    in_table = False

                if current_size + len(stripped) > self.chunk_size and current_size >= self.min_chunk_size:
                    chunks.append('\n'.join(current_table_rows) if in_table else stripped)
                    if not in_table:
                        chunk_metas.append({**metadata, "chunk_type": "spreadsheet"})
                        current_table_rows = []
                    current_size = 0
                else:
                    current_size += len(stripped) + 1

        # 输出剩余内容
        if current_table_rows and table_headers:
            chunks.append('\n'.join([table_headers[-1]] + current_table_rows))
            chunk_metas.append({
                **metadata,
                "table_headers": [table_headers[-1]],
                "chunk_type": "spreadsheet",
            })
        elif current_size >= self.min_chunk_size:
            chunks.append('\n'.join(current_table_rows))
            chunk_metas.append({**metadata, "chunk_type": "spreadsheet"})

        # 如果没有提取到任何块，降级为按段落
        if not chunks:
            return self._fallback_split(text, doc_id, metadata)

        return chunks, chunk_metas

    def _fallback_split(self, text: str, doc_id: str, metadata: Dict) -> Tuple[List[str], List[Dict]]:
        """降级分片"""
        chunks: List[str] = []
        chunk_metas: List[Dict] = []
        current = []
        current_size = 0

        for para in text.split('\n\n'):
            para = para.strip()
            if not para:
                continue
            if current_size + len(para) > self.chunk_size and current_size >= self.min_chunk_size:
                chunks.append('\n\n'.join(current))
                chunk_metas.append({**metadata, "chunk_type": "spreadsheet"})
                current = [para]
                current_size = len(para)
            else:
                current.append(para)
                current_size += len(para) + 2

        if current_size >= self.min_chunk_size:
            chunks.append('\n\n'.join(current))
            chunk_metas.append({**metadata, "chunk_type": "spreadsheet"})

        return chunks, chunk_metas


# ============================================================================
# 策略三: Notes 分片（自然段落 + 标题关键词）
# ============================================================================

class NotesChunkingStrategy(ChunkingStrategy):
    """
    笔记类分片策略

    设计原则：保留语义连贯性，检测标题关键词划分段落

    规则：
    - 检测标题关键词（问题/方法/步骤/原因等）
    - 按自然段落累积，标题处自然切分
    - 不过度切割短段落，保证语义完整
    """

    # 标题关键词（可作为段落开头的词）
    HEADING_KEYWORDS = [
        r'^\d+[\.、]?\s*',                    # 1. 2. 或 1、2、
        r'^第[一二三四五六七八九十\d]+[章节部篇条点]',  # 第一章、第一节
        r'^[【\[](.+?)[】\]]\s*:?',            # 【标题】或 [标题]
        r'^\([一二三四五六七八九十\d]+\)',       # (一) (二)
        r'^\[[^\]]{2,10}\]',                  # [标题] 短标题
        r'^[A-Z][\.、]\s+',                    # A. B. 或 A、B
    ]
    HEADING_PATTERN = re.compile('|'.join(HEADING_KEYWORDS), re.MULTILINE)

    def split(
        self,
        text: str,
        doc_id: str,
        metadata: Dict,
    ) -> Tuple[List[str], List[Dict]]:
        text = self._normalize_whitespace(text)

        lines = text.split('\n')
        chunks: List[str] = []
        chunk_metas: List[Dict] = []

        current_para: List[str] = []
        current_size = 0
        current_heading: Optional[str] = None

        def flush():
            nonlocal current_para, current_size, current_heading
            if not current_para:
                return
            text_block = '\n'.join(current_para).strip()
            if len(text_block) >= self.min_chunk_size:
                chunks.append(text_block)
                meta = {**metadata, "chunk_type": "notes"}
                if current_heading:
                    meta["section_heading"] = current_heading
                chunk_metas.append(meta)
            current_para = []
            current_size = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                current_para.append('')
                continue

            is_heading = bool(self.HEADING_PATTERN.match(stripped))

            if is_heading:
                # 保存当前段落
                flush()

                # 更新当前标题
                heading_text = self.HEADING_PATTERN.match(stripped).group(0) + stripped[len(self.HEADING_PATTERN.match(stripped).group(0)):].strip()
                current_heading = heading_text[:50]
                current_para = [stripped]
                current_size = len(stripped)
            else:
                # 检查是否达到切分阈值
                if current_size + len(stripped) > self.chunk_size and current_size >= self.min_chunk_size:
                    flush()
                    # overlap
                    if current_para:
                        overlap = current_para[-1:]
                        current_para = overlap + [stripped]
                        current_size = sum(len(l) for l in current_para)
                    else:
                        current_para = [stripped]
                        current_size = len(stripped)
                else:
                    current_para.append(stripped)
                    current_size += len(stripped) + 1

        flush()

        # 降级：段落太碎时合并
        if len(chunks) > 20:
            merged: List[str] = []
            merged_metas: List[Dict] = []
            buffer: List[str] = []
            buffer_size = 0
            for chunk, meta in zip(chunks, chunk_metas):
                buffer.append(chunk)
                buffer_size += len(chunk)
                if buffer_size >= self.chunk_size * 0.7:
                    merged.append('\n\n'.join(buffer))
                    merged_metas.append({**metadata, "chunk_type": "notes"})
                    buffer = []
                    buffer_size = 0
            if buffer:
                merged.append('\n\n'.join(buffer))
                merged_metas.append({**metadata, "chunk_type": "notes"})
            return merged, merged_metas

        return chunks, chunk_metas


# ============================================================================
# 通用分片策略（降级）
# ============================================================================

class GenericChunkingStrategy(ChunkingStrategy):
    """通用分片策略（用于未知类型或配置类文档）"""

    def split(
        self,
        text: str,
        doc_id: str,
        metadata: Dict,
    ) -> Tuple[List[str], List[Dict]]:
        text = self._normalize_whitespace(text)

        chunks: List[str] = []
        chunk_metas: List[Dict] = []
        current_lines: List[str] = []
        current_size = 0

        for para in text.split('\n\n'):
            para = para.strip()
            if not para:
                continue

            if current_size + len(para) > self.chunk_size and current_size >= self.min_chunk_size:
                chunks.append('\n\n'.join(current_lines))
                chunk_metas.append({**metadata, "chunk_type": "generic"})
                overlap = current_lines[-(self.chunk_overlap // 30):] if current_lines else []
                current_lines = overlap + [para]
                current_size = sum(len(l) for l in current_lines)
            else:
                current_lines.append(para)
                current_size += len(para) + 2

        if current_size >= self.min_chunk_size:
            chunks.append('\n\n'.join(current_lines))
            chunk_metas.append({**metadata, "chunk_type": "generic"})

        return chunks, chunk_metas


# ============================================================================
# 主分片器
# ============================================================================

class ParentChildChunker:
    """
    文档分片器 — 统一入口

    架构：
    1. 根据文档类型选择专用分片策略（article / spreadsheet / notes / generic）
    2. 在选中的策略内部完成"父文档 + 子文档"双层分片
    3. 自动提取标签（AutoTagger）
    4. 子文档通过 parent_id 引用父文档

    设计原则：
    - 表格数据不破坏行列结构
    - 笔记数据保留语义连贯性
    - 文章数据按章节层级切分
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        parent_chunk_size: int = 2000,
        min_chunk_size: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.parent_chunk_size = parent_chunk_size
        self.min_chunk_size = min_chunk_size

        # 初始化各策略
        self.strategies: Dict[DocType, ChunkingStrategy] = {
            DocType.ARTICLE: ArticleChunkingStrategy(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                parent_chunk_size=parent_chunk_size,
                min_chunk_size=min_chunk_size,
            ),
            DocType.SPREADSHEET: SpreadsheetChunkingStrategy(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                parent_chunk_size=parent_chunk_size,
                min_chunk_size=min_chunk_size,
            ),
            DocType.NOTES: NotesChunkingStrategy(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                parent_chunk_size=parent_chunk_size,
                min_chunk_size=min_chunk_size,
            ),
            DocType.CONFIG: GenericChunkingStrategy(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                parent_chunk_size=parent_chunk_size,
                min_chunk_size=min_chunk_size,
            ),
            DocType.UNKNOWN: GenericChunkingStrategy(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                parent_chunk_size=parent_chunk_size,
                min_chunk_size=min_chunk_size,
            ),
        }

    def chunk(
        self,
        text: str,
        doc_id: str = "",
        title: str = "",
        metadata: Dict = None,
        doc_type: Optional[DocType] = None,
    ) -> ChunkingResult:
        """
        执行文档分片

        Args:
            text: 待分片文本
            doc_id: 文档 ID
            title: 文档标题
            metadata: 额外元数据
            doc_type: 文档类型（若不提供则自动检测）

        Returns:
            ChunkingResult: 分片结果（含父子文档块）
        """
        if not doc_id:
            doc_id = str(uuid.uuid4())

        metadata = dict(metadata) if metadata else {}

        # 0. 自动标签提取（如果 metadata 中没有提供 tags，则自动提取）
        if "tags" not in metadata or not metadata["tags"]:
            tags = AutoTagger.extract_tags(text, title)
            metadata["tags"] = tags
            logger.debug(f"Doc {doc_id} auto-tagged: {tags}")
        else:
            # 保留用户传入的 tags，不自动覆盖
            tags = metadata["tags"]
            logger.debug(f"Doc {doc_id} using provided tags: {tags}")

        # 1. 检测或使用指定的文档类型
        if doc_type is None:
            doc_type = self._detect_doc_type(text, metadata)

        metadata["doc_type"] = doc_type.value

        # 2. 执行策略分片（得到原始文本块）
        strategy = self.strategies.get(doc_type, self.strategies[DocType.UNKNOWN])
        raw_chunks, raw_metas = strategy.split(text, doc_id, metadata)

        # 3. 生成父文档（合并原始块为父块）
        parent_chunks = self._create_parent_chunks(
            raw_chunks, raw_metas, doc_id, metadata
        )

        # 4. 生成子文档（从父文档进一步切分，带父子关系）
        child_chunks = self._create_child_chunks(
            parent_chunks, doc_id, metadata
        )

        total_chars = sum(len(c.content) for c in parent_chunks + child_chunks)

        logger.info(
            f"文档 {doc_id} 分片完成 [type={doc_type.value}]: "
            f"{len(parent_chunks)} 个父文档, {len(child_chunks)} 个子文档, "
            f"共 {total_chars} 字符, tags={tags}"
        )

        return ChunkingResult(
            doc_id=doc_id,
            doc_type=doc_type,
            parent_chunks=parent_chunks,
            child_chunks=child_chunks,
            total_chars=total_chars,
        )

    def _detect_doc_type(self, text: str, metadata: Dict) -> DocType:
        """根据文本特征检测文档类型"""
        # 从元数据覆盖检测
        if metadata.get("doc_type"):
            try:
                return DocType(metadata["doc_type"])
            except ValueError:
                pass

        text_lower = text.lower()
        lines = text.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]

        # 表格特征：| 分隔行占比高
        table_row_count = len([l for l in lines if re.match(r'^\s*\|', l.strip())])
        tab_row_count = len([l for l in lines if '\t' in l and l.strip()])
        if table_row_count > len(non_empty_lines) * 0.2 or tab_row_count > 3:
            return DocType.SPREADSHEET

        # Markdown 标题密度
        md_heading_count = len(re.findall(r'^#{1,6}\s+', text, re.MULTILINE))
        if md_heading_count >= 2:
            return DocType.ARTICLE

        # 笔记特征：短段落 + 标题关键词
        avg_line_len = sum(len(l) for l in non_empty_lines) / max(len(non_empty_lines), 1)
        if avg_line_len < 80 and non_empty_lines:
            notes_keywords = ['总结', '笔记', '要点', '问题', '方法', '步骤', '原因', '结果', '经验', '分享']
            if any(kw in text_lower for kw in notes_keywords):
                return DocType.NOTES

        # 配置类特征
        config_indicators = ['=', ':', '{', '}', '[', ']', 'config', 'setting', '配置', '参数']
        kv_ratio = len(re.findall(r'[:=\[]\s*[^\n]{0,100}', text)) / max(len(non_empty_lines), 1)
        if kv_ratio > 0.3:
            return DocType.CONFIG

        # 默认：文章类
        return DocType.ARTICLE

    def _create_parent_chunks(
        self,
        raw_chunks: List[str],
        raw_metas: List[Dict],
        doc_id: str,
        metadata: Dict,
    ) -> List[TextChunk]:
        """将原始文本块合并为父文档块"""
        parent_chunks = []
        chunks: List[str] = []
        chunk_metas: List[Dict] = []
        current_size = 0

        for chunk_text, chunk_meta in zip(raw_chunks, raw_metas):
            if current_size + len(chunk_text) > self.parent_chunk_size and chunks:
                parent_text = '\n\n'.join(chunks)
                idx = len(parent_chunks)
                chunk_id = f"{doc_id}_parent_{idx}"
                parent_chunks.append(TextChunk(
                    chunk_id=chunk_id,
                    content=parent_text,
                    chunk_index=idx,
                    parent_id=None,
                    is_parent=True,
                    metadata={
                        **metadata,
                        "chunk_type": "parent",
                        "position": idx,
                        "total_parents": 0,  # 暂定，后续更新
                        "tags": metadata.get("tags", []),
                        "section_headings": chunk_metas[-1].get("section_headings", []) if chunk_metas else [],
                    }
                ))
                chunks = []
                chunk_metas = []
                current_size = 0

            chunks.append(chunk_text)
            chunk_metas.append(chunk_meta)
            current_size += len(chunk_text) + 2

        if chunks:
            parent_text = '\n\n'.join(chunks)
            idx = len(parent_chunks)
            chunk_id = f"{doc_id}_parent_{idx}"
            parent_chunks.append(TextChunk(
                chunk_id=chunk_id,
                content=parent_text,
                chunk_index=idx,
                parent_id=None,
                is_parent=True,
                metadata={
                    **metadata,
                    "chunk_type": "parent",
                    "position": idx,
                    "total_parents": len(parent_chunks),
                    "tags": metadata.get("tags", []),
                    "section_headings": chunk_metas[-1].get("section_headings", []) if chunk_metas else [],
                }
            ))

        # 更新 total_parents
        total = len(parent_chunks)
        for pc in parent_chunks:
            pc.metadata["total_parents"] = total

        return parent_chunks

    def _create_child_chunks(
        self,
        parent_chunks: List[TextChunk],
        doc_id: str,
        metadata: Dict,
    ) -> List[TextChunk]:
        """从父文档生成子文档（带父子关系）"""
        child_chunks = []
        child_index = 0

        for parent in parent_chunks:
            parent_text = parent.content

            if len(parent_text) <= self.chunk_size:
                chunk_id = f"{doc_id}_child_{child_index}"
                child_chunks.append(TextChunk(
                    chunk_id=chunk_id,
                    content=parent_text,
                    chunk_index=child_index,
                    parent_id=parent.chunk_id,
                    is_parent=False,
                    metadata={
                        **metadata,
                        "chunk_type": "child",
                        "position": child_index,
                        "parent_position": parent.chunk_index,
                        "tags": metadata.get("tags", []),
                    }
                ))
                child_index += 1
            else:
                sub_chunks = self._split_large_chunk(parent_text)
                for j, sub_text in enumerate(sub_chunks):
                    if len(sub_text) < self.min_chunk_size:
                        continue
                    chunk_id = f"{doc_id}_child_{child_index}"
                    child_chunks.append(TextChunk(
                        chunk_id=chunk_id,
                        content=sub_text,
                        chunk_index=child_index,
                        parent_id=parent.chunk_id,
                        is_parent=False,
                        metadata={
                            **metadata,
                            "chunk_type": "child",
                            "position": child_index,
                            "parent_position": parent.chunk_index,
                            "sub_position": j,
                            "tags": metadata.get("tags", []),
                        }
                    ))
                    child_index += 1

        return child_chunks

    def _split_large_chunk(self, text: str) -> List[str]:
        """分割大文本块（按段落切分）"""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            if end < len(text):
                search_end = min(end + 100, len(text))
                # 优先按段落切分
                sep_pos = text.rfind('\n\n', start + self.chunk_size // 2, search_end)
                if sep_pos > start + self.chunk_size // 2:
                    end = sep_pos + 2

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - self.chunk_overlap
            if start < 0:
                start = 0

        return chunks

    def chunk_texts(
        self,
        texts: List[str],
        doc_id: str = "",
        metadata: Dict = None,
        doc_type: Optional[DocType] = None,
    ) -> List[TextChunk]:
        """
        批量分片（用于短文本）

        Args:
            texts: 文本列表
            doc_id: 文档 ID
            metadata: 元数据
            doc_type: 文档类型

        Returns:
            子文档块列表
        """
        if not doc_id:
            doc_id = str(uuid.uuid4())

        result = self.chunk(
            '\n\n'.join(texts),
            doc_id,
            metadata=metadata or {},
            doc_type=doc_type or DocType.NOTES,
        )
        return result.child_chunks


# ============================================================================
# 便捷函数 & 全局实例
# ============================================================================

_default_chunker: Optional[ParentChildChunker] = None


def get_chunker() -> ParentChildChunker:
    """获取全局分片器"""
    global _default_chunker
    if _default_chunker is None:
        _default_chunker = ParentChildChunker()
    return _default_chunker


def chunk(
    text: str,
    doc_id: str = "",
    title: str = "",
    metadata: Dict = None,
    doc_type: Optional[str] = None,
) -> ChunkingResult:
    """便捷函数：执行文档分片"""
    dt = DocType(doc_type) if doc_type else None
    return get_chunker().chunk(text, doc_id, title, metadata, dt)


def extract_tags(text: str, title: str = "", max_tags: int = 5) -> List[str]:
    """便捷函数：提取标签"""
    return AutoTagger.extract_tags(text, title, max_tags)


def extract_query_keywords(query: str, max_keywords: int = 5) -> List[str]:
    """便捷函数：从查询中提取关键词"""
    return AutoTagger.extract_keywords_from_query(query, max_keywords)
