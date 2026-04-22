"""
飞书模块配置
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings

from config.settings import settings as global_settings


class FeishuSettings(BaseSettings):
    """飞书配置"""

    FEISHU_APP_ID: str = ""
    FEISHU_APP_SECRET: str = ""
    FEISHU_VERIFICATION_TOKEN: str = ""

    FEISHU_BOT_NAME: str = "AI 助手"
    FEISHU_BOT_ICON_URL: str = ""

    FEISHU_WEBHOOK_PATH: str = "/feishu/webhook"
    FEISHU_DEFAULT_SKILL_ID: Optional[str] = None

    FEISHU_ENABLE_STREAMING: bool = False
    FEISHU_MAX_HISTORY_MESSAGES: int = 10

    FEISHU_RATE_LIMIT_PER_MINUTE: int = 20

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


feishu_settings = FeishuSettings()


def reload_from_global_settings():
    """从全局设置同步飞书配置"""
    feishu_settings.FEISHU_APP_ID = global_settings.FEISHU_APP_ID or feishu_settings.FEISHU_APP_ID
    feishu_settings.FEISHU_APP_SECRET = global_settings.FEISHU_APP_SECRET or feishu_settings.FEISHU_APP_SECRET
    feishu_settings.FEISHU_VERIFICATION_TOKEN = global_settings.FEISHU_VERIFICATION_TOKEN or feishu_settings.FEISHU_VERIFICATION_TOKEN
    feishu_settings.FEISHU_WEBHOOK_PATH = global_settings.FEISHU_WEBHOOK_PATH or feishu_settings.FEISHU_WEBHOOK_PATH
    feishu_settings.FEISHU_ENABLE_STREAMING = global_settings.FEISHU_ENABLE_STREAMING or feishu_settings.FEISHU_ENABLE_STREAMING
    feishu_settings.FEISHU_RATE_LIMIT_PER_MINUTE = global_settings.FEISHU_RATE_LIMIT_PER_MINUTE or feishu_settings.FEISHU_RATE_LIMIT_PER_MINUTE


reload_from_global_settings()
