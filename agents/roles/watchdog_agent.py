# -*- coding: utf-8 -*-
"""
WatchdogAgent: basic guardrails (timeouts/memory ceilings).
Future: subprocess isolation and hard limits.
"""
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
import time
from agents.core.base_agent import BaseAgent, AgentResult

@dataclass
class WatchConfig:
    max_seconds: float = 20.0

class WatchdogAgent(BaseAgent):
    role = "watchdog"

    def run(self, **kwargs) -> AgentResult:
        cfg = WatchConfig(max_seconds=float(kwargs.get("max_seconds", self.config.get("max_seconds", 20.0))))
        started = kwargs.get("started_ts", time.time())
        if (time.time() - started) > cfg.max_seconds:
            return AgentResult(ok=False, error=f"Timeout > {cfg.max_seconds}s")
        return AgentResult(ok=True, data={"within_budget": True})

