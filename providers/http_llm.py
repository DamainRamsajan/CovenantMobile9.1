# -*- coding: utf-8 -*-
"""
HTTP provider that talks to:
- llama.cpp server (e.g., /completion or /v1/chat/completions)
- OpenAI-compatible endpoints

Reads env via Django settings:
  MODEL_ENDPOINT: base URL (e.g., http://127.0.0.1:11434 or http://localhost:8080)
  MODEL_NAME:     optional model name for chat APIs
  MODEL_API_KEY:  optional bearer token for secured endpoints
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from dataclasses import dataclass
import requests
from django.conf import settings

from .llm_provider import LLMProvider

DEFAULT_TIMEOUT = 60

@dataclass
class HttpConfig:
    endpoint: str
    model: str = "local"
    api_key: Optional[str] = None
    timeout: int = DEFAULT_TIMEOUT

class HttpLLM(LLMProvider):
    def __init__(self, endpoint: Optional[str] = None, model: Optional[str] = None, api_key: Optional[str] = None, timeout: Optional[int] = None):
        self.cfg = HttpConfig(
            endpoint=(endpoint or (getattr(settings, "MODEL_ENDPOINT", "") or "")).rstrip("/"),
            model=(model or getattr(settings, "MODEL_NAME", "local")),
            api_key=(api_key or getattr(settings, "MODEL_API_KEY", None)),
            timeout=int(timeout or DEFAULT_TIMEOUT),
        )

    # ---------- public API ----------

    def generate(self, prompt: str, **kw) -> str:
        if not self.cfg.endpoint:
            return "[MODEL_ENDPOINT not configured]"
        # headers
        headers = {"Content-Type": "application/json"}
        if self.cfg.api_key:
            headers["Authorization"] = f"Bearer {self.cfg.api_key}"

        # 1) Try llama.cpp style /completion (simple)
        try:
            payload = {
                "prompt": prompt,
                "n_predict": kw.get("max_tokens", 512),
                "temperature": kw.get("temperature", 0.2),
                "stop": kw.get("stop"),
            }
            url = f"{self.cfg.endpoint}/completion"
            r = requests.post(url, json=payload, headers=headers, timeout=self.cfg.timeout)
            if r.ok:
                j = r.json()
                # common llama.cpp field names
                for key in ("content", "text", "response"):
                    if key in j and isinstance(j[key], str):
                        return j[key]
        except Exception as e:
            pass

        # 2) Try OpenAI-compatible /v1/chat/completions
        try:
            data = {
                "model": kw.get("model", self.cfg.model),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kw.get("temperature", 0.2),
                "max_tokens": kw.get("max_tokens", 512),
                "top_p": kw.get("top_p", 1.0),
                "stream": False,
            }
            url = f"{self.cfg.endpoint}/v1/chat/completions"
            r = requests.post(url, json=data, headers=headers, timeout=self.cfg.timeout)
            if r.ok:
                j = r.json()
                if isinstance(j, dict) and "choices" in j and j["choices"]:
                    return j["choices"][0]["message"]["content"]
                # some servers return { "text": "..." }
                if "text" in j:
                    return j["text"]
                return str(j)
            return f"[HTTP {r.status_code}] {r.text[:200]}"
        except Exception as e:
            return f"[Provider error: {e}]"

    def health(self) -> Dict[str, Any]:
        info: Dict[str, Any] = {"ok": False, "provider": "HttpLLM", "endpoint": self.cfg.endpoint}
        if not self.cfg.endpoint:
            info["reason"] = "MODEL_ENDPOINT not set"
            return info
        try:
            # Try a lightweight GET on the root or /health if it exists
            for path in ("/health", "/version", "/"):
                url = f"{self.cfg.endpoint}{path}"
                try:
                    r = requests.get(url, timeout=5)
                    if r.ok:
                        info["ok"] = True
                        info["status"] = r.text[:200]
                        return info
                except Exception:
                    continue
            # If all else fails, mark reachable via a short POST to /completion with small prompt
            try:
                r = requests.post(f"{self.cfg.endpoint}/completion",
                                  json={"prompt": "ping", "n_predict": 1},
                                  timeout=5)
                info["ok"] = r.ok
                info["status"] = "completion ping ok" if r.ok else f"HTTP {r.status_code}"
            except Exception as e:
                info["reason"] = str(e)
        except Exception as e:
            info["reason"] = str(e)
        return info

