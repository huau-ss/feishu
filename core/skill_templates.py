"""
Skill 模板引擎
根据员工的 Skill 配置，动态构建个性化的 RAG 回答 Prompt
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

from llm import ChatMessage

logger = logging.getLogger(__name__)


@dataclass
class SkillProfile:
    """Skill 配置文件"""
    skill_id: str
    name: str
    answer_style: str
    temperature: float
    max_tokens: int
    system_prompt_suffix: str
    knowledge_scope: List[str]
    matched_tags: List[str] = None

    def __post_init__(self):
        if self.matched_tags is None:
            self.matched_tags = []


class SkillTemplateEngine:
    """
    Skill 模板引擎

    负责根据 Skill 配置和查询上下文，动态生成个性化的系统提示词和检索策略。

    核心设计：
    - 不同的 Skill 定义了不同的回答风格（严谨/高效/新人友好）
    - 每个 Skill 可以有不同的 temperature、max_tokens、知识范围过滤器
    - 引擎负责将这些配置转化为 RAG 引擎可用的参数
    """

    STYLE_HINTS = {
        "rigorous": {
            "detail_level": "high",
            "structure": "hierarchical",
            "requires_citation": True,
            "requires_steps": True,
            "requires_prerequisites": True,
            "emoji_prefix": "🔬",
            "tag_to_style": {
                "运维": "回答要注重操作步骤的清晰性和可执行性，包含具体的命令和配置示例。",
                "部署": "回答要包含详细的部署流程、环境要求和注意事项。",
                "产品": "回答要注重产品特性、规格参数和选型建议，条理清晰。",
                "开发": "回答要包含技术原理、代码示例和最佳实践。",
                "安全": "回答要强调安全风险、防护措施和合规要求。",
                "数据库": "回答要包含具体的SQL语句、表结构设计和优化建议。",
                "财务": "回答要注重数据的准确性，提供清晰的费用明细和计费逻辑。",
                "技术支持": "回答要结构化，优先给出解决步骤，必要时给出排查路径。",
            },
        },
        "efficient": {
            "detail_level": "medium",
            "structure": "bullets",
            "requires_citation": False,
            "requires_steps": False,
            "requires_prerequisites": False,
            "emoji_prefix": "⚡",
            "tag_to_style": {
                "运维": "给出运维操作的核心框架和关键风险点即可。",
                "部署": "给出部署方案的核心架构和关键节点。",
                "产品": "给出产品选型的关键决策维度。",
                "开发": "给出技术方案的核心设计思路和关键权衡点。",
                "安全": "给出安全方案的核心防护层次和关键注意点。",
                "数据库": "给出数据库设计的核心原则和优化方向。",
                "财务": "给出财务分析的核心维度和关键指标。",
                "技术支持": "给出技术支持的核心判断路径和关键节点。",
            },
        },
        "beginner": {
            "detail_level": "high",
            "structure": "friendly",
            "requires_citation": False,
            "requires_steps": True,
            "requires_prerequisites": False,
            "emoji_prefix": "🌱",
            "tag_to_style": {
                "运维": "用通俗的语言解释运维操作，每个步骤都要详细说明。",
                "部署": "用日常生活比喻解释部署过程，让新手能理解。",
                "产品": "用简单易懂的语言介绍产品功能，避免专业术语。",
                "开发": "用教学式的风格解释开发概念，假设读者完全不懂。",
                "安全": "用生活中的安全常识来比喻信息安全。",
                "数据库": "用图书馆或Excel来比喻数据库，让非技术人员也能理解。",
                "财务": "用简单的日常生活例子来解释财务概念。",
                "技术支持": "用问诊式的风格耐心解答，假设用户是第一次接触。",
            },
        },
        "balanced": {
            "detail_level": "medium",
            "structure": "paragraph",
            "requires_citation": True,
            "requires_steps": False,
            "requires_prerequisites": False,
            "emoji_prefix": "⚖️",
            "tag_to_style": {
                "运维": "回答要注重操作步骤的清晰性和可执行性。",
                "部署": "回答要包含部署流程和关键注意事项。",
                "产品": "回答要注重产品特性和选型建议。",
                "开发": "回答要包含技术原理和最佳实践。",
                "安全": "回答要强调安全风险和防护措施。",
                "数据库": "回答要包含SQL语句和优化建议。",
                "财务": "回答要注重数据准确性和费用明细。",
                "技术支持": "回答要结构化，给出解决步骤。",
            },
        },
    }

    def __init__(self):
        self._style_cache: Dict[str, Dict] = {}

    def build_system_prompt(
        self,
        base_prompt: str,
        skill_profile: SkillProfile,
        query: str = "",
    ) -> str:
        """
        根据 Skill 配置构建完整的系统提示词

        Args:
            base_prompt: 基础提示词（来自 RAG Engine）
            skill_profile: Skill 配置文件
            query: 用户查询（用于上下文感知）

        Returns:
            个性化后的完整系统提示词
        """
        style = self.STYLE_HINTS.get(skill_profile.answer_style, self.STYLE_HINTS["balanced"])

        parts = [base_prompt.strip()]

        if skill_profile.system_prompt_suffix:
            parts.append("\n\n" + skill_profile.system_prompt_suffix)

        tag_style_additions = []
        for tag in skill_profile.matched_tags:
            if tag in style["tag_to_style"]:
                tag_style_additions.append(style["tag_to_style"][tag])

        if tag_style_additions:
            parts.append(
                "\n\n【当前问题领域补充要求】\n" +
                "\n".join(f"- {s}" for s in tag_style_additions)
            )

        return "\n\n".join(parts)

    def build_retrieval_filter(
        self,
        skill_profile: SkillProfile,
    ) -> Optional[Dict[str, Any]]:
        """
        根据 Skill 的知识范围构建检索过滤器

        Args:
            skill_profile: Skill 配置文件

        Returns:
            Qdrant 过滤器字典，或 None（无过滤）
        """
        if not skill_profile.knowledge_scope:
            return None

        return {
            "should": [
                {
                    "key": "tags",
                    "match": {"value": tag},
                }
                for tag in skill_profile.knowledge_scope
            ],
            "min_should_match": 1,
        }

    def format_answer(
        self,
        raw_answer: str,
        skill_profile: SkillProfile,
        sources: List[Dict] = None,
        query: str = "",
    ) -> str:
        """
        对原始回答进行后处理，应用 Skill 特定的格式风格

        Args:
            raw_answer: LLM 生成的原始回答
            skill_profile: Skill 配置文件
            sources: 参考来源列表
            query: 原始问题

        Returns:
            格式化后的回答文本
        """
        style = self.STYLE_HINTS.get(skill_profile.answer_style, self.STYLE_HINTS["balanced"])

        formatted = raw_answer

        if style["structure"] == "hierarchical":
            if not raw_answer.startswith("#") and not raw_answer.startswith("**"):
                pass

        if style["requires_citation"] and sources:
            citation_needed = True
            for src in sources:
                if src.get("title") and src["title"] not in formatted:
                    citation_note = f"\n\n_以上内容参考: {src['title']}_"
                    if citation_note not in formatted:
                        formatted = formatted.rstrip() + citation_note
                        break

        return formatted

    def estimate_context_tokens(
        self,
        chunks: List[Any],
        max_tokens: int,
    ) -> List[Any]:
        """
        根据 Skill 的 max_tokens 限制，智能裁剪上下文

        Args:
            chunks: 检索到的文档块列表
            max_tokens: 最大 token 数

        Returns:
            裁剪后的块列表
        """
        import tiktoken

        try:
            enc = tiktoken.get_encoding("cl100k_base")
        except Exception:
            return chunks[:3]

        selected = []
        total_tokens = 0

        for chunk in chunks:
            chunk_text = getattr(chunk, "content", str(chunk))
            chunk_tokens = len(enc.encode(chunk_text))

            if total_tokens + chunk_tokens > max_tokens:
                remaining = max_tokens - total_tokens
                if remaining > 200:
                    truncated = enc.decode(enc.encode(chunk_text)[:remaining])
                    chunk.content = truncated
                    selected.append(chunk)
                break

            selected.append(chunk)
            total_tokens += chunk_tokens

        return selected

    def get_llm_params(
        self,
        skill_profile: SkillProfile,
    ) -> Dict[str, Any]:
        """
        获取 LLM 调用参数

        Args:
            skill_profile: Skill 配置文件

        Returns:
            LLM 参数字典（temperature, max_tokens 等）
        """
        return {
            "temperature": skill_profile.temperature,
            "max_tokens": skill_profile.max_tokens,
        }


_default_engine: Optional[SkillTemplateEngine] = None


def get_skill_template_engine() -> SkillTemplateEngine:
    global _default_engine
    if _default_engine is None:
        _default_engine = SkillTemplateEngine()
    return _default_engine
