# -*- coding: utf-8 -*-
"""
Covenant Mobile v9.1 — agents/core/base_agent.py
Base Agent contract: configure -> run -> result
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
import time
import uuid

@dataclass
class AgentResult:
    ok: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: str = ""

class BaseAgent:
    role: str = "base"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.agent_id = f"{self.role}:{uuid.uuid4().hex[:8]}"

    def configure(self, **kwargs) -> None:
        self.config.update(kwargs or {})

    def run(self, **kwargs) -> AgentResult:
        """
        Override in subclasses. Must return AgentResult.
        """
        return AgentResult(ok=True, data={"msg":"noop"})

    # tiny helper for timing
    def _timed(self, fn, *a, **kw) -> tuple[float, Any]:
        t0 = time.perf_counter()
        out = fn(*a, **kw)
        return (time.perf_counter() - t0, out)

