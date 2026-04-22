"""
飞书 API 客户端
封装飞书开放平台 API：消息发送、用户信息获取等
"""

import time
import json
import logging
from typing import Optional, Dict, Any, List

import httpx

from feishu.config import feishu_settings

logger = logging.getLogger(__name__)


class FeishuAPIError(Exception):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(f"Feishu API Error {code}: {msg}")


class FeishuClient:
    """飞书开放平台 API 客户端"""

    BASE_URL = "https://open.feishu.cn/open-apis"

    def __init__(
        self,
        app_id: str = None,
        app_secret: str = None,
    ):
        self.app_id = app_id or feishu_settings.FEISHU_APP_ID
        self.app_secret = app_secret or feishu_settings.FEISHU_APP_SECRET
        self._tenant_access_token = None
        self._token_expires_at = 0.0
        self._client = httpx.Client(timeout=30.0)

    def _get_token(self) -> str:
        if self._tenant_access_token and time.time() < self._token_expires_at - 60:
            return self._tenant_access_token

        resp = self._client.post(
            f"{self.BASE_URL}/auth/v3/tenant_access_token/internal",
            json={
                "app_id": self.app_id,
                "app_secret": self.app_secret,
            },
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != 0:
            raise FeishuAPIError(data.get("code"), data.get("msg", ""))

        self._tenant_access_token = data["tenant_access_token"]
        self._token_expires_at = time.time() + data.get("expire", 7200)
        return self._tenant_access_token

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
        }

    def _post(self, path: str, data: Dict, params: Dict = None) -> Dict:
        resp = self._client.post(
            f"{self.BASE_URL}{path}",
            json=data,
            headers=self._headers(),
            params=params,
        )
        try:
            result = resp.json()
        except Exception:
            resp.raise_for_status()
            raise FeishuAPIError(resp.status_code, resp.text)
        if result.get("code") != 0:
            logger.warning(f"Feishu API error on {path}: {result}")
            raise FeishuAPIError(result.get("code"), result.get("msg", ""))
        if resp.status_code >= 400:
            resp.raise_for_status()
        return result.get("data", {})

    def _get(self, path: str, params: Dict = None) -> Dict:
        resp = self._client.get(
            f"{self.BASE_URL}{path}",
            params=params,
            headers=self._headers(),
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise FeishuAPIError(result.get("code"), result.get("msg", ""))
        return result.get("data", {})

    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """获取用户基本信息"""
        return self._get("/contact/v3/users/" + user_id, params={"user_id_type": "open_id"})

    def get_user_list(self, department_id: str = "", page_size: int = 50) -> List[Dict]:
        """获取部门下用户列表"""
        params = {"user_id_type": "open_id", "page_size": page_size}
        if department_id:
            params["department_id"] = department_id
        return self._get("/contact/v3/users", params=params).get("items", [])

    def send_text_message(self, receive_id: str, content: str) -> Dict:
        """
        发送文本消息

        Args:
            receive_id: 接收者 open_id 或群组 chat_id
            content: 文本内容

        Returns:
            消息发送结果
        """
        if receive_id.startswith("oc_"):
            receive_id_type = "chat_id"
        elif receive_id.startswith("ou_"):
            receive_id_type = "open_id"
        elif len(receive_id) == 36 and "-" in receive_id:
            receive_id_type = "chat_id"
        else:
            receive_id_type = "chat_id" if len(receive_id) > 16 else "open_id"
        content_str = json.dumps({"text": content}, ensure_ascii=False)
        return self._post(
            "/im/v1/messages",
            {
                "receive_id": receive_id,
                "msg_type": "text",
                "content": content_str,
            },
            params={"receive_id_type": receive_id_type},
        )

    def send_interactive_card(
        self,
        receive_id: str,
        card_content: Dict,
        update_multi: bool = False,
    ) -> Dict:
        """
        发送交互式卡片消息

        Args:
            receive_id: 接收者 open_id 或群组 chat_id
            card_content: 卡片 JSON 内容
            update_multi: 是否更新多个消息

        Returns:
            消息发送结果
        """
        if receive_id.startswith("oc_"):
            receive_id_type = "chat_id"
        elif receive_id.startswith("ou_"):
            receive_id_type = "open_id"
        elif len(receive_id) == 36 and "-" in receive_id:
            receive_id_type = "chat_id"
        else:
            receive_id_type = "chat_id" if len(receive_id) > 16 else "open_id"

        params = {"receive_id_type": receive_id_type}
        if update_multi:
            params["receive_id"] = receive_id

        return self._post(
            "/im/v1/messages",
            {
                "receive_id": receive_id,
                "msg_type": "interactive",
                "content": card_content
                if isinstance(card_content, str)
                else json.dumps(card_content, ensure_ascii=False),
            },
            params=params,
        )

    def reply_message(
        self,
        message_id: str,
        content: str,
        msg_type: str = "text",
    ) -> Dict:
        """回复指定消息"""
        if msg_type == "text":
            content = json.dumps({"text": content}, ensure_ascii=False)
        return self._post(
            f"/im/v1/messages/{message_id}/reply",
            {
                "msg_type": msg_type,
                "content": content,
            },
        )

    def build_text_card(
        self,
        header_text: str = "",
        answer: str = "",
        sources: List[Dict] = None,
        employee_name: str = "",
        skill_name: str = "",
        source_label: str = "知识库",
    ) -> Dict:
        """
        构建文本卡片消息

        Args:
            header_text: 卡片标题
            answer: 回答内容
            sources: 参考来源列表
            employee_name: 员工名称
            skill_name: 当前 Skill 名称
            source_label: 来源标签

        Returns:
            卡片 JSON 字符串
        """
        elements = [
            {
                "tag": "markdown",
                "content": answer,
            },
        ]

        if sources:
            source_lines = []
            for i, s in enumerate(sources[:3], 1):
                title = s.get("title", "未知文档")
                score = s.get("score", 0)
                source_lines.append(f"- {i}. **{title}** (相关度: {score:.0%})")
            if source_lines:
                elements.append({
                    "tag": "markdown",
                    "content": f"\n---\n**{source_label}**\n" + "\n".join(source_lines),
                })

        footer_text = f"via {skill_name}" if skill_name else ""
        if employee_name:
            footer_text = f"{employee_name} · AI 助手" if footer_text else f"AI 助手 · {employee_name}"

        elements.append({
            "tag": "note",
            "elements": [
                {"tag": "plain_text", "content": footer_text or "AI 助手"},
            ],
        })

        card = {
            "config": {
                "wide_screen_mode": True,
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": header_text or "AI 助手回复",
                },
                "template": "blue",
            },
            "elements": elements,
        }

        return json.dumps(card)

    def build_stream_card(
        self,
        header_text: str = "AI 助手回复",
        answer: str = "",
    ) -> Dict:
        """构建流式更新用的简化卡片"""
        return {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": header_text},
                "template": "blue",
            },
            "elements": [
                {"tag": "markdown", "content": answer},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "正在思考..."}]},
            ],
        }

    def update_message(self, message_id: str, card_content: Dict) -> Dict:
        """更新消息（用于流式更新）"""
        return self._patch(
            f"/im/v1/messages/{message_id}",
            {
                "msg_type": "interactive",
                "content": card_content
                if isinstance(card_content, str)
                else json.dumps(card_content, ensure_ascii=False),
            },
        )

    def _patch(self, path: str, data: Dict) -> Dict:
        resp = self._client.patch(
            f"{self.BASE_URL}{path}",
            json=data,
            headers=self._headers(),
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") != 0:
            raise FeishuAPIError(result.get("code"), result.get("msg", ""))
        return result.get("data", {})

    def get_bot_info(self) -> Dict:
        """获取机器人信息"""
        return self._get("/bot/v3/info")


_default_client: Optional[FeishuClient] = None


def get_feishu_client() -> FeishuClient:
    global _default_client
    if _default_client is None:
        _default_client = FeishuClient()
    return _default_client
