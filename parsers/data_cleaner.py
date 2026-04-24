"""
数据清洗模块
支持多格式差异化清洗：PDF / TXT / Excel / Word / CSV / XML / RTF / ZIP / 视频音频
"""
import re
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class PDFType(Enum):
    """PDF 三种分类"""
    MARKETING_WHITEPAPER = "marketing_whitepaper"   # 营销白皮书（多栏排版）
    WEB_EXPORT = "web_export"                       # 网页导出型（URL、单栏）
    COMMUNITY_LEADGEN = "community_leadgen"          # 社区引流型（干货+广告）


@dataclass
class CleanResult:
    """清洗结果"""
    title: str                                        # 文档标题
    content: str                                      # 清洗后正文
    doc_type: str                                     # 文档类型: article/spec_sheet/price_list/config_file
    pdf_type: Optional[PDFType] = None                # PDF 类型（仅 PDF 有值）
    metadata: Dict = field(default_factory=dict)       # 额外元数据
    warnings: List[str] = field(default_factory=list) # 警告信息


# ============================================================================
# PDF 三分类检测器
# ============================================================================

class PDFTypeDetector:
    """
    PDF 三分类检测器

    Type 1 - 营销白皮书 (marketing_whitepaper): 多栏排版
    Type 2 - 网页导出型 (web_export): URL / 单栏
    Type 3 - 社区引流型 (community_leadgen): 干货+广告
    """

    # Type 1 特征
    MULTI_COLUMN_INDICATORS = [
        r'【.{0,20}】',    # 章节符号 【背景】【目标】
        r'第[一二三四五六七八九十\d]+部分',
        r'CHAPTER\s+\d+',
        r'Part\s+[IVX\d]+',
        r'\d+\.\d+\.\d+',  # 1.2.3 多级编号
        r'[一二三四五六七八九十]+、',  # 中文列表
    ]

    # Type 2 特征
    WEB_EXPORT_INDICATORS = [
        r'https?://',
        r'www\.',
        r'\.com|\.cn|\.org|\.net',
        r'上一页|下一页|返回目录',
        r'浏览量|阅读量|点赞',
        r'发布时间|更新时间',
        r'©\s*\d{4}|Copyright',
        r'京ICP备|ICP备',
    ]

    # Type 3 特征
    LEADGEN_QUALITY_INDICATORS = [
        r'技术分享|实战|经验|总结',
        r'原理|架构|设计|实现',
        r'安装|配置|部署',
        r'代码|示例|demo',
        r'问题|解决|方案',
        r'教程|指南|手册',
    ]

    LEADGEN_AD_INDICATORS = [
        r'扫码|二维码|关注|公众号',
        r'加微|商务合作|咨询',
        r'限时|优惠|折扣|促销',
        r'立即购买|点击获取',
        r'转发|分享|邀请',
        r'抽奖|中奖|福利',
        r'广告',
        r'联系\s*[\u4e00-\u9fa5]{2,10}\s*[0-9]',
        r'联系\s*我|加我',
        r'技术支持|售前|售后',
        r'业务截断|更多内容',
        r'完整版|获取全文',
    ]

    @classmethod
    def detect(cls, text: str, filename: str = "", metadata: Optional[Dict] = None) -> PDFType:
        """
        检测 PDF 类型

        Args:
            text: PDF 文本内容
            filename: 文件名（用于辅助判断）
            metadata: 从 PDF 提取的元数据（如页数、尺寸等）

        Returns:
            PDFType 分类结果
        """
        text_lower = text.lower()
        filename_lower = filename.lower()

        # 辅助数据
        meta = metadata or {}
        page_count = meta.get('page_count', 0)
        lines = text.split('\n')
        non_short_lines = [l for l in lines if len(l.strip()) > 20]
        avg_line_len = sum(len(l) for l in non_short_lines) / max(len(non_short_lines), 1)

        # ----- Type 1: 营销白皮书 -----
        # 特征：多栏排版指标 + 文件名含白皮书相关词
        multi_col_score = 0
        for pattern in cls.MULTI_COLUMN_INDICATORS:
            if re.search(pattern, text):
                multi_col_score += 1

        marketing_keywords = ['白皮书', 'whitepaper', '产品手册', 'datasheet', 'specification', 'brochure']
        has_marketing_kw = any(kw in filename_lower for kw in marketing_keywords)
        if has_marketing_kw:
            multi_col_score += 2

        # 多级编号段落密度高
        numbered_pattern_count = len(re.findall(r'\d+\.\d+(?:\.\d+)?', text))
        if numbered_pattern_count > 10:
            multi_col_score += 1

        if multi_col_score >= 2:
            return PDFType.MARKETING_WHITEPAPER

        # ----- Type 2: 网页导出型 -----
        # 特征：URL + 单栏布局 + 短行 + 互联网标识
        web_score = 0

        url_count = len(re.findall(r'https?://\S+', text_lower))
        if url_count >= 2:
            web_score += 2

        for pattern in cls.WEB_EXPORT_INDICATORS:
            if re.search(pattern, text, re.IGNORECASE):
                web_score += 1

        # 单栏特征：平均行长度适中，无大量列表编号
        if 30 <= avg_line_len <= 80:
            web_score += 1

        # 短段落多（网页特征）
        short_para_ratio = len([l for l in lines if 10 <= len(l.strip()) <= 50]) / max(len(lines), 1)
        if short_para_ratio > 0.4:
            web_score += 1

        # 文档较短
        if page_count > 0 and page_count <= 10:
            web_score += 1

        if web_score >= 3:
            return PDFType.WEB_EXPORT

        # ----- Type 3: 社区引流型 -----
        # 特征：干货指标 + 广告/引流指标并存
        quality_score = 0
        ad_score = 0

        for pattern in cls.LEADGEN_QUALITY_INDICATORS:
            if re.search(pattern, text):
                quality_score += 1

        for pattern in cls.LEADGEN_AD_INDICATORS:
            if re.search(pattern, text):
                ad_score += 1

        # 技术文档比例高但末尾有引流
        quality_ratio = quality_score / max(quality_score + ad_score, 1)
        if quality_score >= 2 and ad_score >= 1:
            return PDFType.COMMUNITY_LEADGEN

        # 默认：页面多且内容长 → 白皮书
        if page_count > 10:
            return PDFType.MARKETING_WHITEPAPER

        # 默认：短文档 → 网页导出
        return PDFType.WEB_EXPORT


# ============================================================================
# TXT 清洗器
# ============================================================================

class TXTDataCleaner:
    """
    TXT 文件专用清洗规则：

    - 提取并规范化头部元数据
    - 删除重复段落（如"联系技术支持"）
    - 删除口语化引导语
    - 清理格式噪声
    """

    # 重复引导段落
    REPEAT_PARAGRAPHS = [
        r'联系\s*[\u4e00-\u9fa5]{0,10}\s*[0-9]{3,}',
        r'如需\s*帮助|如有\s*疑问|如有\s*问题',
        r'更多\s*信息|更多\s*内容',
        r'关注\s*我们|扫描\s*二维码',
        r'转发|分享|收藏',
        r'版权\s*所有|Copyright.*?\d{4}',
        r'此文档\s*由.*?生成',
        r'最后\s*更新|更新时间',
        r'本文件\s*仅供.*?使用',
        r'免责声明',
        r'此页\s*空白|此页\s*无\s*内容',
    ]

    # 口语化引导语
    SPOKEN_GUIDES = [
        r'^大家好',
        r'^各位\s*好',
        r'^今天\s*我们',
        r'^下面\s*介绍',
        r'^首先',
        r'^其次',
        r'^最后\s*一点',
        r'^总之',
        r'^总的\s*来说',
        r'^OK[，,]',
        r'^嗯',
        r'^这个\s*东西',
        r'^那个\s*东西',
        r'^嗯哼',
        r'^好的[，,]',
        r'^嗯嗯',
        r'^hello',
        r'^hi[，,]',
        r'^hi\s+',
    ]

    # 头部元数据模式
    HEADER_METADATA_PATTERNS = [
        (r'标题[：:]\s*(.+)', 'title'),
        (r'作者[：:]\s*(.+)', 'author'),
        (r'日期[：:]\s*(.+)', 'date'),
        (r'版本[：:]\s*(.+)', 'version'),
        (r'分类[：:]\s*(.+)', 'category'),
    ]

    # 格式噪声
    FORMAT_NOISE = [
        r'\*{3,}',     # ****
        r'-{3,}',      # ----
        r'={3,}',      # ====
        r'_{3,}',      # ____
        r'\.{3,}',     # ....
        r'^\s*>\s*$',  # 空引用
        r'^\s*#+\s*$', # 空标题标记
    ]

    def clean(self, text: str, filename: str = "") -> Tuple[str, Dict]:
        """
        清洗 TXT 文件

        Returns:
            (清洗后文本, 提取的元数据)
        """
        lines = text.split('\n')
        cleaned_lines = []
        metadata = {}

        # 1. 提取头部元数据
        metadata, text = self._extract_header_metadata(text)

        # 2. 删除重复段落
        text = self._remove_repeat_paragraphs(text)

        # 3. 删除口语化引导语
        text = self._remove_spoken_guides(text)

        # 4. 清理格式噪声
        text = self._remove_format_noise(text)

        # 5. 规范化空白和换行
        text = self._normalize_whitespace(text)

        return text, metadata

    def _extract_header_metadata(self, text: str) -> Tuple[Dict, str]:
        """提取头部元数据"""
        metadata = {}
        lines = text.split('\n')
        content_lines = []
        header_found = False

        for i, line in enumerate(lines[:15]):
            matched = False
            for pattern, key in self.HEADER_METADATA_PATTERNS:
                m = re.match(pattern, line.strip())
                if m:
                    metadata[key] = m.group(1).strip()
                    matched = True
                    header_found = True
                    break
            if not matched:
                content_lines.append(line)

        if header_found:
            return metadata, '\n'.join(content_lines)
        return metadata, text

    def _remove_repeat_paragraphs(self, text: str) -> str:
        """删除重复段落"""
        # 统计段落出现频次
        lines = text.split('\n')
        line_counts: Dict[str, int] = {}
        for line in lines:
            key = re.sub(r'\s+', '', line.strip().lower())
            if len(key) > 10:
                line_counts[key] = line_counts.get(key, 0) + 1

        result_lines = []
        for line in lines:
            key = re.sub(r'\s+', '', line.strip().lower())
            if len(key) > 10 and line_counts.get(key, 0) >= 3:
                continue  # 出现3次以上的段落跳过
            result_lines.append(line)

        text = '\n'.join(result_lines)

        # 按模式删除
        for pattern in self.REPEAT_PARAGRAPHS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)

        return text

    def _remove_spoken_guides(self, text: str) -> str:
        """删除口语化引导语"""
        for pattern in self.SPOKEN_GUIDES:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        return text

    def _remove_format_noise(self, text: str) -> str:
        """清理格式噪声"""
        for pattern in self.FORMAT_NOISE:
            text = re.sub(pattern, '', text, flags=re.MULTILINE)
        return text

    def _normalize_whitespace(self, text: str) -> str:
        """规范化空白"""
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
        return text


# ============================================================================
# PDF 差异化清洗器
# ============================================================================

class PDFDataCleaner:
    """
    PDF 文件差异化清洗规则：

    Type 1 - 营销白皮书: 线性重组与语境缝合
      - 识别并拼接多栏布局段落
      - 恢复文档结构层级

    Type 2 - 网页导出型: 断句连贯与外围去噪
      - 修复意外截断的句子
      - 去除页眉页脚和导航元素

    Type 3 - 社区引流型: 业务截断与实体格式化
      - 在引流/广告前截断内容
      - 保留干货，提取技术实体
    """

    # 营销白皮书 - 结构化元素
    CHAPTER_PATTERNS = [
        r'【([^】]+)】',
        r'第[一二三四五六七八九十\d]+[章节部篇]',
        r'CHAPTER\s+(\d+)',
        r'PART\s+[IVX\d]+',
        r'\n(#+\s+.+)',
    ]

    # 社区引流型 - 引流/广告截断点
    LEADGEN_BREAK_PATTERNS = [
        r'扫码\s*关注|扫描\s*二维码',
        r'关注\s*公众号|商务\s*合作',
        r'如需\s*获取\s*完整版|获取\s*完整版',
        r'广告|Advertisement',
        r'加微信号|添加\s*微信',
        r'限时优惠|立即购买',
        r'转发|分享|邀请',
        r'抽奖|福利|赠送',
        r'---{3,}|\\*{3,}',
        r'业务截断',
    ]

    # 通用页眉页脚
    HEADER_FOOTER_PATTERNS = [
        r'^\d+\s*$',              # 仅页码
        r'^第\s*\d+\s*页$',
        r'^-{5,}$',               # 分隔线
    ]

    def clean_type1_marketing(self, text: str) -> str:
        """
        清洗 Type 1: 营销白皮书
        策略：线性重组与语境缝合
        """
        lines = text.split('\n')
        result_lines = []

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # 检测章节标题
            is_chapter = False
            for pattern in self.CHAPTER_PATTERNS:
                if re.search(pattern, line):
                    result_lines.append(f'\n## {line}')
                    is_chapter = True
                    break

            # 合并被意外拆分的短行（< 15字符的孤立行可能是多栏拼接产物）
            if not is_chapter and len(line) < 15 and result_lines:
                prev = result_lines[-1].strip()
                if prev and not prev.startswith('#') and len(prev) > 30:
                    result_lines[-1] = prev + ' ' + line
                    continue

            result_lines.append(line)

        text = '\n'.join(result_lines)
        text = self._remove_headers_footers(text)
        text = self._normalize_whitespace(text)
        return text

    def clean_type2_web_export(self, text: str) -> str:
        """
        清洗 Type 2: 网页导出型
        策略：断句连贯与外围去噪
        """
        # 1. 去除 URL 噪声（保留 URL 文本，删除裸链接格式）
        text = re.sub(r'<(https?://[^>]+)>', r'\1', text)
        text = re.sub(r'\[(https?://[^\]]+)\]\([^\)]+\)', r'\1', text)

        # 2. 修复被截断的句子（行末无标点 + 下一行首字小写 = 续接）
        lines = text.split('\n')
        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                fixed_lines.append('')
                i += 1
                continue

            # 如果行末没有终止标点，尝试与下一行合并
            if i + 1 < len(lines) and line and line[-1] not in '。！？；.!?,;':
                next_line = lines[i + 1].strip()
                if next_line and next_line[0].islower():
                    line = line + ' ' + next_line
                    i += 2
                else:
                    fixed_lines.append(line)
                    i += 1
            else:
                fixed_lines.append(line)
                i += 1

        text = '\n'.join(fixed_lines)

        # 3. 去除导航/版权等外围噪声
        nav_noise = [
            r'上一页|下一页|返回目录|返回列表',
            r'浏览量[：:]\s*\d+',
            r'阅读量[：:]\s*\d+',
            r'©\s*\d{4}.*?$',
            r'Copyright.*$',
            r'京ICP备\d+-?\d+号',
            r'ICP备\d+-?\d+号',
        ]
        for pattern in nav_noise:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)

        text = self._remove_headers_footers(text)
        text = self._normalize_whitespace(text)
        return text

    def clean_type3_community(self, text: str) -> str:
        """
        清洗 Type 3: 社区引流型
        策略：业务截断与实体格式化
        """
        # 1. 在引流点之前截断
        for pattern in self.LEADGEN_BREAK_PATTERNS:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                # 保留引流点之前的内容，但留下提示
                text = text[:m.start()]
                break

        # 2. 提取并保留技术实体（代码片段、配置、命令）
        # 格式化为结构化块
        code_patterns = [
            (r'`([^`]+)`', r'[代码块: \1]'),
            (r'```[\s\S]*?```', '[代码块]'),
            (r'\$\s*(\w[\w\s\-]+)', r'[命令: \1]'),
        ]
        for pattern, replacement in code_patterns:
            text = re.sub(pattern, replacement, text)

        # 3. 规范化技术术语格式
        tech_formats = [
            (r'\b([A-Z][a-z]+[A-Z]\w+)', r'[产品: \1]'),  # 驼峰格式
            (r'\b(v?\d+\.\d+\.\d+\w?)', r'[版本: \1]'),   # 版本号
            (r'\b(\w+@\w+\.\w+)', r'[邮箱: \1]'),         # 邮箱
        ]
        for pattern, replacement in tech_formats:
            text = re.sub(pattern, replacement, text)

        text = self._remove_headers_footers(text)
        text = self._normalize_whitespace(text)
        return text

    def clean(self, text: str, pdf_type: PDFType) -> str:
        """根据 PDF 类型调用对应清洗策略"""
        if pdf_type == PDFType.MARKETING_WHITEPAPER:
            return self.clean_type1_marketing(text)
        elif pdf_type == PDFType.WEB_EXPORT:
            return self.clean_type2_web_export(text)
        elif pdf_type == PDFType.COMMUNITY_LEADGEN:
            return self.clean_type3_community(text)
        return text

    def _remove_headers_footers(self, text: str) -> str:
        """移除页眉页脚"""
        lines = text.split('\n')
        cleaned_lines = []
        seen_headers = {}
        seen_footers = {}

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                cleaned_lines.append(stripped)
                continue

            # 页眉：文档开头连续几行重复出现
            if i < 5 and len(stripped) < 60:
                seen_headers[stripped] = seen_headers.get(stripped, 0) + 1
                if seen_headers.get(stripped, 0) > 2 and len(seen_headers) <= 3:
                    continue

            # 页脚：文档末尾重复出现
            if i >= len(lines) - 5 and len(stripped) < 60:
                seen_footers[stripped] = seen_footers.get(stripped, 0) + 1
                if seen_footers.get(stripped, 0) > 2 and len(seen_footers) <= 2:
                    continue

            # 跳过仅包含分隔符的行
            if re.match(r'^\s*[-=_~]{3,}\s*$', stripped):
                continue

            cleaned_lines.append(stripped)

        return '\n'.join(cleaned_lines)

    def _normalize_whitespace(self, text: str) -> str:
        """规范化空白"""
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text


# ============================================================================
# Excel / Word 表格清洗器
# ============================================================================

class TableDataCleaner:
    """
    Excel / Word 文件专用清洗规则：

    - 保留表格结构
    - 清理格式符号
    """

    def clean(self, text: str, file_type: str = "") -> str:
        """
        清洗 Excel / Word 表格文件
        """
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 清理 Excel/WORD 残留格式符号
            line = self._clean_format_symbols(line)

            # 如果是表格行，规范化分隔符
            if '|' in line or '\t' in line:
                line = self._normalize_table_row(line)

            cleaned_lines.append(line)

        # 规范化空白
        result = '\n'.join(cleaned_lines)
        result = re.sub(r'\n{3,}', '\n\n', result)
        return result

    def _clean_format_symbols(self, line: str) -> str:
        """清理格式符号"""
        noise = [
            (r'[{}\[\]]', ''),          # 括号
            (r'\s+', ' '),              # 多余空格
            (r'^[\s\-=~]+|[\s\-=~]+$', ''),  # 首尾分隔符
        ]
        for pattern, replacement in noise:
            line = re.sub(pattern, replacement, line)
        return line.strip()

    def _normalize_table_row(self, line: str) -> str:
        """规范化表格行"""
        # 统一分隔符为 |
        if '\t' in line:
            cells = line.split('\t')
            line = ' | '.join(c.strip() for c in cells if c.strip())

        # 清理单元格内多余空格
        if '|' in line:
            cells = line.split('|')
            line = '|'.join(c.strip() for c in cells)

        return line


# ============================================================================
# CSV 表格清洗器
# ============================================================================

class CSVDataCleaner:
    """
    CSV 文件专用清洗规则：

    - 清理首尾空白字符
    - 规范化分隔符
    - 统一单元格格式
    - 去除重复行
    """

    def clean(self, text: str) -> Tuple[str, Dict]:
        """
        清洗 CSV 文件

        Returns:
            (清洗后文本, 元数据字典)
        """
        metadata: Dict = {}
        lines = text.split('\n')
        cleaned_lines = []
        seen = set()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            normalized = re.sub(r'\s+', '', line)
            if normalized in seen:
                continue
            seen.add(normalized)

            cells = line.split(',')
            cleaned_cells = []
            for cell in cells:
                cell = cell.strip()
                cell = re.sub(r'^\s+|\s+$', '', cell)
                cell = re.sub(r'\s{2,}', ' ', cell)
                if cell.startswith('"') and cell.endswith('"'):
                    cell = cell[1:-1]
                if cell.startswith("'") and cell.endswith("'"):
                    cell = cell[1:-1]
                cleaned_cells.append(cell)

            cleaned_lines.append(', '.join(cleaned_cells))

        metadata['row_count'] = len(cleaned_lines)
        result = '\n'.join(cleaned_lines)
        return result, metadata


# ============================================================================
# XML 清洗器
# ============================================================================

class XMLDataCleaner:
    """
    XML 文件专用清洗规则：

    - 移除 XML 声明和注释
    - 规范化标签缩进（转为纯文本）
    - 清理属性噪声
    """

    def clean(self, text: str) -> Tuple[str, Dict]:
        """
        清洗 XML 文件

        Returns:
            (清洗后文本, 元数据字典)
        """
        metadata: Dict = {}

        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith('[') and ']' in stripped:
                continue

            if stripped.startswith('@'):
                continue

            cleaned_lines.append(stripped)

        result = '\n'.join(cleaned_lines)
        result = re.sub(r'^\s+|\s+$', '', result, flags=re.MULTILINE)
        result = re.sub(r'\n{3,}', '\n\n', result)

        metadata['format'] = 'xml'
        return result, metadata


# ============================================================================
# RTF 清洗器
# ============================================================================

class RTFDataCleaner:
    """
    RTF 文件专用清洗规则：

    - 移除 RTF 控制词
    - 清理字体和颜色指令
    - 规范化换行
    """

    def clean(self, text: str) -> Tuple[str, Dict]:
        """
        清洗 RTF 文件

        Returns:
            (清洗后文本, 元数据字典)
        """
        result = text

        result = re.sub(r'\\[a-z]+\d*\s?|\{[^}]*\}', '', result)
        result = re.sub(r"\\'([0-9a-fA-F]{2})", lambda m: chr(int(m.group(1), 16)), result)
        result = re.sub(r'\n{3,}', '\n\n', result)
        result = re.sub(r'^\s+|\s+$', '', result, flags=re.MULTILINE)
        result = re.sub(r'[ \t]+', ' ', result)

        metadata: Dict = {}
        return result, metadata


# ============================================================================
# 主数据清洗器
# ============================================================================

class DataCleaner:
    """
    主数据清洗器 — 统一入口

    根据文件类型分发到专用清洗器：

    - TXT   → TXTDataCleaner
    - PDF   → PDFDataCleaner（差异化）
    - Excel / Word → TableDataCleaner
    - CSV   → CSVDataCleaner
    - XML   → XMLDataCleaner
    - RTF   → RTFDataCleaner
    - ZIP   → 通用清洗（内部文件已由ZIPParser处理）
    - 视频/音频 → 通用清洗（Whisper转写已清洗）
    - 其他  → 通用清洗
    """

    GARBAGE_PATTERNS = [
        r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]',
        r'[\ufffd]+',
        r'\ufffd',
    ]

    SPEC_KEYWORDS = [
        '型号', 'processor', 'cpu', '内存', 'memory', '硬盘', 'storage', 'disk',
        '规格', '配置', '接口', 'port', '电源', 'power', '网络', 'network',
        '尺寸', 'dimension', '重量', 'weight', '参数', 'specification',
        '处理器', 'cores', '线程', 'frequency', '频率', '缓存', 'cache',
    ]

    PRICE_KEYWORDS = [
        '价格', 'price', '单价', '报价', 'cost', '费用', '预算', 'budget',
        '¥', 'rmb', 'dollar', '$', '元', '角', '分', '万元', '千元',
        '成交价', '批发价', '零售价', '采购价', '市场价',
    ]

    def __init__(self):
        self.garbage_compiled = [re.compile(p) for p in self.GARBAGE_PATTERNS]
        self.txt_cleaner = TXTDataCleaner()
        self.pdf_cleaner = PDFDataCleaner()
        self.table_cleaner = TableDataCleaner()
        self.csv_cleaner = CSVDataCleaner()
        self.xml_cleaner = XMLDataCleaner()
        self.rtf_cleaner = RTFDataCleaner()

    def clean(
        self,
        text: str,
        filename: str = "",
        file_type: str = "",
        pdf_type: Optional[PDFType] = None,
    ) -> CleanResult:
        """
        清洗文本

        Args:
            text: 原始文本
            filename: 文件名（用于提取标题）
            file_type: 文件类型 (pdf/txt/xlsx/docx/xml/zip/csv/rtf/mp4/...)
            pdf_type: PDF 类型（从 PDFTypeDetector 检测获得）

        Returns:
            CleanResult: 清洗结果
        """
        warnings = []

        # 0. 移除乱码
        text = self._remove_garbage(text)

        # 1. 提取标题
        title = self._extract_title(text, filename)

        # 2. 格式专用清洗
        file_type_lower = file_type.lower()
        if file_type_lower == 'txt':
            text, extracted_meta = self.txt_cleaner.clean(text, filename)
        elif file_type_lower in ('xlsx', 'xls', 'csv', 'docx', 'doc'):
            text = self.table_cleaner.clean(text, file_type_lower)
            extracted_meta = {}
        elif file_type_lower == 'csv':
            text, extracted_meta = self.csv_cleaner.clean(text)
        elif file_type_lower == 'xml':
            text, extracted_meta = self.xml_cleaner.clean(text)
        elif file_type_lower == 'rtf':
            text, extracted_meta = self.rtf_cleaner.clean(text)
        elif file_type_lower == 'pdf':
            # 检测 PDF 类型（如果未提供）
            if pdf_type is None:
                pdf_type = PDFTypeDetector.detect(text, filename)
                warnings.append(f"自动检测 PDF 类型: {pdf_type.value}")
            text = self.pdf_cleaner.clean(text, pdf_type)
            extracted_meta = {"pdf_type": pdf_type.value}
        elif file_type_lower in ('zip', 'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm',
                                  'mp3', 'wav', 'm4a', 'flac', 'ogg'):
            # ZIP/视频/音频：Whisper或ZIP解析器已做初步处理，只做通用清洗
            text = self._generic_clean(text)
            extracted_meta = {}
        else:
            # 通用清洗
            text = self._generic_clean(text)
            extracted_meta = {}

        # 3. 检测文档类型
        doc_type = self._detect_doc_type(text, file_type)

        # 4. 提取元数据
        metadata = self._extract_metadata(text, doc_type)
        metadata.update(extracted_meta)

        # 5. 去重
        text = text.strip()

        return CleanResult(
            title=title,
            content=text,
            doc_type=doc_type,
            pdf_type=pdf_type,
            metadata=metadata,
            warnings=warnings,
        )

    def _remove_garbage(self, text: str) -> str:
        """移除乱码字符"""
        for pattern in self.garbage_compiled:
            text = pattern.sub('', text)
        return text

    def _extract_title(self, text: str, filename: str) -> str:
        """从文本或文件名提取标题"""
        lines = text.split('\n')

        for line in lines[:10]:
            line = line.strip()
            if len(line) > 5 and len(line) < 200:
                if not line.startswith('[') and not line.startswith('#'):
                    if not any(c in line for c in ['|', '---', '***']):
                        return line[:200]

        if filename:
            name = Path(filename).stem
            name = name.replace('_', ' ').replace('-', ' ')
            return name[:200]

        return "未命名文档"

    def _generic_clean(self, text: str) -> str:
        """通用清洗（用于非特殊格式）"""
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
        return text

    def _detect_doc_type(self, text: str, file_type: str = "") -> str:
        """检测文档类型"""
        text_lower = text.lower()

        if file_type in ['xlsx', 'xls', 'csv']:
            if any(kw in text_lower for kw in self.PRICE_KEYWORDS):
                return 'price_list'
            if any(kw in text_lower for kw in self.SPEC_KEYWORDS):
                return 'spec_sheet'
        elif file_type in ['yaml', 'yml', 'json', 'cfg', 'conf', 'ini', 'toml', 'xml']:
            return 'config_file'

        price_score = sum(1 for kw in self.PRICE_KEYWORDS if kw in text_lower)
        spec_score = sum(1 for kw in self.SPEC_KEYWORDS if kw in text_lower)

        if price_score >= 2:
            return 'price_list'
        elif spec_score >= 3:
            return 'spec_sheet'

        return 'article'

    def _extract_metadata(self, text: str, doc_type: str) -> Dict:
        """提取元数据"""
        metadata = {}

        if doc_type in ['spec_sheet', 'config_file']:
            key_values = self._extract_key_values(text)
            metadata['key_values'] = key_values
            brand_model = self._extract_brand_model(text)
            metadata.update(brand_model)

        if doc_type == 'price_list':
            tables = self._extract_tables(text)
            metadata['tables'] = tables

        return metadata

    def _extract_key_values(self, text: str) -> Dict[str, str]:
        """提取键值对"""
        key_values = {}
        patterns = [
            r'([\u4e00-\u9fa5a-zA-Z][\u4e00-\u9fa5a-zA-Z0-9\s]{0,30}?)\s*[:：＝=]\s*([^\n]{1,200})',
            r'([\u4e00-\u9fa5a-zA-Z]{2,20}?)\s*\|\s*([^\n]{1,200})',
        ]
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                key = match.group(1).strip()
                value = match.group(2).strip()
                if len(key) > 1 and len(value) > 0:
                    key_values[key] = value[:200]
        return dict(list(key_values.items())[:50])

    def _extract_brand_model(self, text: str) -> Dict[str, str]:
        """提取品牌和型号"""
        result = {}
        brands = [
            'Dell', 'HP', 'HPE', 'Lenovo', 'Huawei', 'Inspur', '浪潮',
            'Cisco', 'Juniper', 'Arista', 'H3C', 'TP-Link',
            'Intel', 'AMD', 'NVIDIA', 'Samsung', 'Micron',
            'Western Digital', 'WD', 'Seagate',
        ]
        for brand in brands:
            if brand.lower() in text.lower():
                result['brand'] = brand
                break
        model_patterns = [
            r'([A-Z][a-zA-Z0-9\-]+(?:[0-9]+[a-zA-Z]?)?(?:\s*[Vv]\d+)?(?:\s*[A-Z]\d+)?)',
            r'(PowerEdge\s*[A-Z]\d+[a-zA-Z0-9]*)',
            r'(ThinkSystem\s*[A-Z][A-Z0-9\-]+)',
        ]
        for pattern in model_patterns:
            match = re.search(pattern, text)
            if match:
                result['model'] = match.group(1)
                break
        return result

    def _extract_tables(self, text: str) -> List[List[str]]:
        """提取表格数据"""
        tables = []
        lines = text.split('\n')
        current_table = []

        for line in lines:
            line = line.strip()
            if '|' in line:
                cells = [cell.strip() for cell in line.split('|')]
                cells = [c for c in cells if c]
                if cells:
                    current_table.append(cells)
            else:
                if current_table and len(current_table) > 1:
                    tables.append(current_table)
                current_table = []

        if current_table and len(current_table) > 1:
            tables.append(current_table)

        return tables[:5]

    def remove_duplicates(self, texts: List[str]) -> List[str]:
        """去除重复文本块"""
        if not texts:
            return []

        unique_texts = []
        seen = set()

        for text in texts:
            normalized = re.sub(r'\s+', '', text.lower())[:200]
            if normalized not in seen:
                seen.add(normalized)
                unique_texts.append(text)

        return unique_texts


# ============================================================================
# 便捷函数 & 全局实例
# ============================================================================

_default_cleaner: Optional[DataCleaner] = None


def get_cleaner() -> DataCleaner:
    """获取全局清洗器实例"""
    global _default_cleaner
    if _default_cleaner is None:
        _default_cleaner = DataCleaner()
    return _default_cleaner


def clean(
    text: str,
    filename: str = "",
    file_type: str = "",
    pdf_type: Optional[PDFType] = None,
) -> CleanResult:
    """便捷函数：清洗文本"""
    return get_cleaner().clean(text, filename, file_type, pdf_type)


def detect_pdf_type(text: str, filename: str = "", metadata: Optional[Dict] = None) -> PDFType:
    """检测 PDF 类型"""
    return PDFTypeDetector.detect(text, filename, metadata)
