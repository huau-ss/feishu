"""
飞书个性化 Bot 模块
支持为每个员工配置专属的 AI 回答风格（Skill）
"""

from feishu.bot import FeishuBot
from feishu.client import FeishuClient

__all__ = ["FeishuBot", "FeishuClient"]
