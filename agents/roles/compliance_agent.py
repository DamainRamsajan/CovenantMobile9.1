# -*- coding: utf-8 -*-
"""
ComplianceAgent: runs lightweight allow/deny checks before tool/model use.
Future: OPA/Cedar integration.
"""
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
from agents.core.base_agent import BaseAgent, AgentResult

@dataclass
class ComplianceConfig:
    offline_only: bool = True

class ComplianceAgent(BaseAgent):
    role = "compliance"

    def run(self, **kwargs) -> AgentResult:
        action = (kwargs.get("action") or "").strip()
        context = kwargs.get("context") or {}
        cfg = ComplianceConfig(
            offline_only=bool(kwargs.get("offline_only", self.config.get("offline_only", True)))
        )

        # Minimal rules: deny network if offline-only
        if cfg.offline_only and context.get("requires_network"):
            return AgentResult(ok=False, error="Policy deny: offline-only mode")

        # Allow otherwise
        return AgentResult(ok=True, data={"allowed": True, "action": action})

