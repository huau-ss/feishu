"""
文档解析器模块
支持 PDF, Word, Excel, PPT, TXT, HTML 等格式
"""
import io
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import re

logger = logging.getLogger(__name__)


class BaseParser(ABC):
    """解析器基类"""

    @abstractmethod
    def extract(self, file_path: str | Path) -> str:
        """提取文本内容"""
        pass

    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """支持的扩展名"""
        pass

    def is_supported(self, file_path: str | Path) -> bool:
        """检查是否支持该文件"""
        ext = Path(file_path).suffix.lower()
        return ext in self.supported_extensions


class PDFParser(BaseParser):
    """PDF 解析器"""

    @property
    def supported_extensions(self) -> List[str]:
        return [".pdf"]

    def extract(self, file_path: str | Path) -> str:
        try:
            import pymupdf
        except ImportError:
            raise ImportError("请安装 pymupdf: pip install pymupdf")

        text_parts = []
        with pymupdf.open(file_path) as doc:
            for page_num, page in enumerate(doc, 1):
                text = page.get_text("text")
                if text.strip():
                    text_parts.append(f"[第{page_num}页]\n{text}")

        return "\n\n".join(text_parts)

    def extract_with_metadata(self, file_path: str | Path) -> Tuple[str, Dict]:
        """
        提取文本内容并返回元数据

        Returns:
            (文本内容, 元数据字典)
        """
        try:
            import pymupdf
        except ImportError:
            raise ImportError("请安装 pymupdf: pip install pymupdf")

        text_parts = []
        metadata: Dict = {}

        with pymupdf.open(file_path) as doc:
            metadata['page_count'] = len(doc)
            if doc.metadata:
                pdf_meta = doc.metadata
                metadata['pdf_title'] = pdf_meta.get('title', '')
                metadata['pdf_author'] = pdf_meta.get('author', '')
                metadata['pdf_subject'] = pdf_meta.get('subject', '')

            for page_num, page in enumerate(doc, 1):
                text = page.get_text("text")
                if text.strip():
                    text_parts.append(f"[第{page_num}页]\n{text}")

        return "\n\n".join(text_parts), metadata


class DocxParser(BaseParser):
    """Word 文档解析器"""

    @property
    def supported_extensions(self) -> List[str]:
        return [".docx", ".doc"]

    def extract(self, file_path: str | Path) -> str:
        try:
            from docx import Document
        except ImportError:
            raise ImportError("请安装 python-docx: pip install python-docx")

        doc = Document(file_path)
        paragraphs = []

        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)

        # 提取表格
        for table in doc.tables:
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if cells:
                    paragraphs.append(" | ".join(cells))

        return "\n\n".join(paragraphs)


class ExcelParser(BaseParser):
    """Excel 解析器"""

    @property
    def supported_extensions(self) -> List[str]:
        return [".xlsx", ".xls"]

    def extract(self, file_path: str | Path) -> str:
        try:
            import openpyxl
        except ImportError:
            raise ImportError("请安装 openpyxl: pip install openpyxl")

        text_parts = []
        wb = openpyxl.load_workbook(file_path, data_only=True)

        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            text_parts.append(f"[工作表: {sheet_name}]")

            for row in sheet.iter_rows(values_only=True):
                cells = [str(cell) if cell is not None else "" for cell in row]
                row_text = " | ".join(cells).strip()
                if row_text:
                    text_parts.append(row_text)

            text_parts.append("")

        return "\n".join(text_parts)


class PPTParser(BaseParser):
    """PPT 解析器"""

    @property
    def supported_extensions(self) -> List[str]:
        return [".pptx", ".ppt"]

    def extract(self, file_path: str | Path) -> str:
        try:
            from pptx import Presentation
        except ImportError:
            raise ImportError("请安装 python-pptx: pip install python-pptx")

        prs = Presentation(file_path)
        text_parts = []

        for slide_num, slide in enumerate(prs.slides, 1):
            slide_texts = [f"[幻灯片 {slide_num}]"]

            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_texts.append(shape.text.strip())

            if len(slide_texts) > 1:
                text_parts.append("\n".join(slide_texts))

        return "\n\n".join(text_parts)


class HTMLParser(BaseParser):
    """HTML 解析器"""

    @property
    def supported_extensions(self) -> List[str]:
        return [".html", ".htm"]

    def extract(self, file_path: str | Path) -> str:
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError("请安装 beautifulsoup4: pip install beautifulsoup4")

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n", strip=True)
        return text


class TXTParser(BaseParser):
    """纯文本解析器"""

    @property
    def supported_extensions(self) -> List[str]:
        return [".txt", ".md", ".json", ".yaml", ".yml", ".cfg", ".conf", ".log"]

    def extract(self, file_path: str | Path) -> str:
        encodings = ["utf-8", "gbk", "gb2312", "gb18030", "latin-1"]

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


class EmailParser(BaseParser):
    """邮件解析器 (.eml, .msg)"""

    @property
    def supported_extensions(self) -> List[str]:
        return [".eml", ".msg"]

    def extract(self, file_path: str | Path) -> str:
        text_parts = []

        try:
            import email
            from email import policy

            with open(file_path, "rb") as f:
                msg = email.message_from_binary_file(f, policy=policy.default)

            text_parts.append(f"主题: {msg.get('Subject', '无')}")
            text_parts.append(f"发件人: {msg.get('From', '无')}")
            text_parts.append(f"收件人: {msg.get('To', '无')}")
            text_parts.append("")

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            charset = part.get_content_charset() or "utf-8"
                            text_parts.append(payload.decode(charset, errors="ignore"))
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    charset = msg.get_content_charset() or "utf-8"
                    text_parts.append(payload.decode(charset, errors="ignore"))

        except Exception as e:
            logger.warning(f"解析邮件文件失败 {file_path}: {e}")
            return TXTParser().extract(file_path)

        return "\n".join(text_parts)


class ParserFactory:
    """解析器工厂"""

    def __init__(self):
        self._parsers: List[BaseParser] = [
            PDFParser(),
            DocxParser(),
            ExcelParser(),
            PPTParser(),
            HTMLParser(),
            TXTParser(),
            EmailParser(),
        ]

    def get_parser(self, file_path: str | Path) -> Optional[BaseParser]:
        """根据文件类型获取解析器"""
        for parser in self._parsers:
            if parser.is_supported(file_path):
                return parser
        return None

    def extract(self, file_path: str | Path) -> str:
        """提取文件内容"""
        parser = self.get_parser(file_path)
        if parser is None:
            raise ValueError(f"不支持的文件类型: {Path(file_path).suffix}")

        content = parser.extract(file_path)
        logger.info(f"成功解析文件: {file_path}, 提取文本 {len(content)} 字符")
        return content

    def extract_with_metadata(self, file_path: str | Path) -> Tuple[str, Dict]:
        """
        提取文件内容并返回元数据（仅 PDF 支持）

        Returns:
            (文本内容, 元数据字典)

        Raises:
            ValueError: 不支持的文件类型
        """
        parser = self.get_parser(file_path)
        if parser is None:
            raise ValueError(f"不支持的文件类型: {Path(file_path).suffix}")

        if isinstance(parser, PDFParser):
            content, meta = parser.extract_with_metadata(file_path)
        else:
            content = parser.extract(file_path)
            meta = {}

        logger.info(f"成功解析文件: {file_path}, 提取文本 {len(content)} 字符")
        return content, meta

    def supported_extensions(self) -> List[str]:
        """所有支持的扩展名"""
        extensions = []
        for parser in self._parsers:
            extensions.extend(parser.supported_extensions)
        return list(set(extensions))


# 全局解析器实例
_default_parser: Optional[ParserFactory] = None


def get_parser() -> ParserFactory:
    """获取全局解析器实例"""
    global _default_parser
    if _default_parser is None:
        _default_parser = ParserFactory()
    return _default_parser


def extract(file_path: str | Path) -> str:
    """便捷函数：提取文件内容"""
    return get_parser().extract(file_path)


def extract_with_metadata(file_path: str | Path) -> Tuple[str, Dict]:
    """便捷函数：提取文件内容并返回元数据（仅 PDF 支持）"""
    return get_parser().extract_with_metadata(file_path)
