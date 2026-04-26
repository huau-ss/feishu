"""
外部大模型接口模块
支持 Ollama、OpenAI、Claude、DashScope 等
"""
import json
import logging
import httpx
from typing import Optional, List, Dict, Any, Generator, AsyncGenerator, Iterator
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """LLM 响应"""
    content: str
    model: str
    usage: Dict[str, int] = field(default_factory=dict)
    finish_reason: str = ""
    raw_response: Any = None


@dataclass
class ChatMessage:
    """聊天消息"""
    role: str  # system/user/assistant
    content: str
    name: Optional[str] = None


class BaseLLMClient(ABC):
    """LLM 客户端基类"""

    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        """发送聊天请求"""
        pass

    @abstractmethod
    def stream(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> Generator[str, None, None]:
        """流式生成"""
        pass

    def chat_with_system_prompt(
        self,
        user_message: str,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        """使用系统提示词聊天"""
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=user_message),
        ]
        return self.chat(messages, temperature, max_tokens, **kwargs)


class OllamaClient(BaseLLMClient):
    """Ollama 本地模型客户端"""

    def __init__(
        self,
        model: str = "qwen3-vl:4b",
        base_url: str = "http://localhost:8000",
    ):
        super().__init__(model)
        self.base_url = base_url.rstrip('/')
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import httpx
            self._client = httpx.Client(trust_env=False, timeout=300.0)
        return self._client

    def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        """Ollama 聊天"""
        ollama_messages = []
        for msg in messages:
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "stream": False,
        }

        response = self.client.post(
            f"{self.base_url}/api/chat",
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

        msg_data = result["message"]
        content = msg_data.get("content") or msg_data.get("thinking", "")

        return LLMResponse(
            content=content,
            model=self.model,
            usage={"prompt_tokens": 0, "completion_tokens": 0},
            finish_reason=result.get("done_reason", ""),
            raw_response=result,
        )

    def stream(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> Generator[str, None, None]:
        """Ollama 同步流式生成"""
        ollama_messages = []
        for msg in messages:
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "stream": True,
        }

        with self.client.stream(
            "POST",
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=httpx.Timeout(600.0, connect=30.0),
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data:
                            msg_data = data["message"]
                            content = msg_data.get("content") or msg_data.get("thinking", "")
                            if content:
                                yield content
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue

    async def astream(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Ollama 异步流式生成"""
        import httpx

        ollama_messages = []
        for msg in messages:
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "stream": True,
        }

        async with httpx.AsyncClient(trust_env=False, timeout=300.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json=payload,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if "message" in data:
                                msg_data = data["message"]
                                content = msg_data.get("content") or msg_data.get("thinking", "")
                                if content:
                                    yield content
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue


class OpenAIClient(BaseLLMClient):
    """OpenAI 兼容 API 客户端"""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: str = "",
        base_url: str = "https://api.openai.com/v1",
    ):
        super().__init__(model)
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import httpx
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.Client(headers=headers, trust_env=False, timeout=300.0)
        return self._client

    def _convert_messages(self, messages: List[ChatMessage]) -> List[Dict]:
        """转换消息格式"""
        result = []
        for msg in messages:
            item = {"role": msg.role, "content": msg.content}
            if msg.name:
                item["name"] = msg.name
            result.append(item)
        return result

    def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        """OpenAI 聊天"""
        payload = {
            "model": self.model,
            "messages": self._convert_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        payload.update(kwargs)

        response = self.client.post(
            f"{self.base_url}/chat/completions",
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

        choice = result["choices"][0]
        return LLMResponse(
            content=choice["message"]["content"],
            model=self.model,
            usage=result.get("usage", {}),
            finish_reason=choice.get("finish_reason", ""),
            raw_response=result,
        )

    def stream(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> Generator[str, None, None]:
        """OpenAI 流式生成"""
        payload = {
            "model": self.model,
            "messages": self._convert_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        payload.update(kwargs)

        token_count = 0
        with self.client.stream(
            "POST",
            f"{self.base_url}/chat/completions",
            json=payload,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line and line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        content = data["choices"][0]["delta"].get("content", "")
                        if content:
                            token_count += 1
                            yield content
                    except json.JSONDecodeError:
                        continue
        logger.info(f"OpenAI stream complete, yielded {token_count} tokens")


class ClaudeClient(BaseLLMClient):
    """Anthropic Claude 客户端"""

    def __init__(
        self,
        model: str = "claude-3-5-haiku-20241022",
        api_key: str = "",
    ):
        super().__init__(model)
        self.api_key = api_key
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import httpx
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
            self._client = httpx.Client(headers=headers, trust_env=False, timeout=300.0)
        return self._client

    def _convert_messages(self, messages: List[ChatMessage]) -> str:
        """转换消息为 Claude 格式"""
        parts = []
        for msg in messages:
            if msg.role == "system":
                parts.append(f"\n[系统提示]: {msg.content}")
            elif msg.role == "user":
                parts.append(f"\n[用户]: {msg.content}")
            elif msg.role == "assistant":
                parts.append(f"\n[助手]: {msg.content}")
        return "\n".join(parts)

    def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        """Claude 聊天"""
        system_msg = ""
        chat_messages = []
        for msg in messages:
            if msg.role == "system":
                system_msg += msg.content + "\n"
            else:
                chat_messages.append(msg)

        prompt = self._convert_messages(chat_messages)

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if system_msg:
            payload["system"] = system_msg
        payload.update(kwargs)

        response = self.client.post(
            "https://api.anthropic.com/v1/messages",
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

        return LLMResponse(
            content=result["content"][0]["text"],
            model=self.model,
            usage={
                "input_tokens": result["usage"]["input_tokens"],
                "output_tokens": result["usage"]["output_tokens"],
            },
            finish_reason=result.get("stop_reason", ""),
            raw_response=result,
        )

    def stream(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> Generator[str, None, None]:
        """Claude 流式生成（简化实现）"""
        response = self.chat(messages, temperature, max_tokens, **kwargs)
        for char in response.content:
            yield char


class DashScopeClient(BaseLLMClient):
    """阿里云 DashScope 客户端（通义千问等）"""

    def __init__(
        self,
        model: str = "qwen-plus",
        api_key: str = "",
    ):
        super().__init__(model)
        self.api_key = api_key
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import httpx
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.Client(headers=headers, trust_env=False, timeout=300.0)
        return self._client

    def chat(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> LLMResponse:
        """DashScope 聊天"""
        dashscope_messages = []
        for msg in messages:
            dashscope_messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        payload = {
            "model": self.model,
            "input": {"messages": dashscope_messages},
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "result_format": "message",
            },
        }

        response = self.client.post(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

        output = result["output"]
        return LLMResponse(
            content=output["choices"]["message"]["content"],
            model=self.model,
            usage=output.get("usage", {}),
            finish_reason=output["choices"].get("finish_reason", ""),
            raw_response=result,
        )

    def stream(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs,
    ) -> Generator[str, None, None]:
        """DashScope 流式生成"""
        import urllib.request
        import urllib.error

        dashscope_messages = []
        for msg in messages:
            dashscope_messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        payload = {
            "model": self.model,
            "input": {"messages": dashscope_messages},
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "result_format": "message",
                "incremental_output": True,
            },
        }

        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(
            "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            data=data,
            headers=headers,
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=300) as response:
            for line in response:
                if line:
                    line_str = line.decode("utf-8").strip()
                    if line_str.startswith("data:"):
                        data_str = line_str[5:].strip()
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and "delta" in data["choices"][0]:
                                content = data["choices"][0]["delta"].get("content", "")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue


def create_llm_client(
    provider: str = "ollama",
    model: str = "",
    api_key: str = "",
    base_url: str = "",
) -> BaseLLMClient:
    """
    创建 LLM 客户端

    Args:
        provider: 提供商 (ollama/openai/claude/dashscope)
        model: 模型名称
        api_key: API 密钥
        base_url: API 地址

    Returns:
        BaseLLMClient 实例
    """
    if provider == "ollama":
        return OllamaClient(
            model=model or "qwen3-vl:4b",
            base_url=base_url or "http://localhost:8000",
        )
    elif provider == "openai":
        return OpenAIClient(
            model=model or "gpt-4o-mini",
            api_key=api_key,
            base_url=base_url or "https://api.openai.com/v1",
        )
    elif provider == "claude":
        return ClaudeClient(
            model=model or "claude-3-5-haiku-20241022",
            api_key=api_key,
        )
    elif provider == "dashscope":
        return DashScopeClient(
            model=model or "qwen-plus",
            api_key=api_key,
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")


# 全局实例
_default_client: Optional[BaseLLMClient] = None


def get_llm_client(provider: str = "ollama", **kwargs) -> BaseLLMClient:
    """获取 LLM 客户端"""
    global _default_client
    _default_client = create_llm_client(provider, **kwargs)
    return _default_client
