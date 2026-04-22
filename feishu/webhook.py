"""
飞书 Webhook 处理器
提供 FastAPI 路由处理飞书事件（URL 验证 + 消息回调）
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel

from feishu.bot import FeishuBot, get_feishu_bot
from feishu.config import feishu_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feishu", tags=["飞书 Bot"])

feishu_bot: FeishuBot = None


def init_feishu_bot(bot: FeishuBot):
    global feishu_bot
    feishu_bot = bot


class FeishuChallengeResponse(BaseModel):
    code: int
    challenge: str = None
    msg: str = None


def _process_message_event(event_data: Dict):
    """后台处理消息事件"""
    global feishu_bot
    if feishu_bot is None:
        logger.error("FeishuBot not initialized")
        return

    try:
        result = feishu_bot.handle_message(event_data)
        if result:
            msg = feishu_bot.parse_message(event_data)
            feishu_bot.send_reply(msg, result)
    except Exception as e:
        logger.error(f"Error processing feishu message: {e}", exc_info=True)


@router.api_route("/webhook", methods=["GET", "POST"])
async def feishu_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    飞书 Webhook 统一入口

    GET:  URL 验证（飞书校验回调地址有效性）
    POST: 事件回调（接收飞书推送的事件）
    """
    global feishu_bot
    if feishu_bot is None:
        try:
            feishu_bot = get_feishu_bot()
        except Exception as e:
            logger.error(f"Failed to initialize FeishuBot: {e}")

    # ============ GET 请求：飞书 URL 验证 ============
    if request.method == "GET":
        params = dict(request.query_params)
        challenge = params.get("challenge", "")
        verification_token = params.get("verification_token", "")

        if not challenge:
            from fastapi.responses import JSONResponse
            return JSONResponse(content={"code": 99, "msg": "missing challenge"})

        if verification_token and feishu_settings.FEISHU_VERIFICATION_TOKEN:
            if verification_token != feishu_settings.FEISHU_VERIFICATION_TOKEN:
                from fastapi.responses import JSONResponse
                return JSONResponse(content={"code": 99, "msg": "token mismatch"})

        from fastapi.responses import JSONResponse
        return JSONResponse(content={"code": 0, "challenge": challenge})

    # ============ POST 请求：事件回调 ============
    try:
        body = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse request body: {e}")
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"code": 99, "msg": "invalid json"}, status_code=400)

    print("====== 收到飞书原始数据 ======\n", body, "\n============================")

    event_type = body.get("header", {}).get("event_type", "")
    event_data = body.get("event", {})

    logger.debug(f"Received feishu event: type={event_type}")

    # 事件回调 URL 验证（POST body 中带 challenge）
    if body.get("challenge"):
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"code": 0, "challenge": body.get("challenge")})

    if event_type == "im.message.receive_v1":
        message_obj = event_data.get("message", {})
        sender = event_data.get("sender", {})
        sender_type = sender.get("sender_type", "")
        if sender_type == "bot":
            logger.debug("Skipping bot's own message")
            from fastapi.responses import JSONResponse
            return JSONResponse(content={"code": 0, "msg": "ok"})

        message_type = message_obj.get("message_type", "")
        if message_type not in ("text",):
            logger.debug(f"Skipping non-text message type: {message_type}")
            from fastapi.responses import JSONResponse
            return JSONResponse(content={"code": 0, "msg": "ok"})

        background_tasks.add_task(_process_message_event, event_data)
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"code": 0, "msg": "ok"})

    from fastapi.responses import JSONResponse
    return JSONResponse(content={"code": 0, "msg": "event type not handled"})


@router.get("/health")
async def feishu_health():
    """飞书 Bot 健康检查"""
    global feishu_bot
    if feishu_bot is None:
        return {"status": "not_initialized"}

    try:
        bot_info = feishu_bot.feishu_client.get_bot_info()
        return {
            "status": "ok",
            "bot_name": bot_info.get("bot", {}).get("app_name", ""),
            "feishu_configured": bool(feishu_settings.FEISHU_APP_ID),
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e),
            "feishu_configured": bool(feishu_settings.FEISHU_APP_ID),
        }
