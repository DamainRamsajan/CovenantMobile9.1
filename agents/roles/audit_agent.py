# -*- coding: utf-8 -*-
"""
AuditAgent: records run steps; hash-chained provenance later.
"""
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
import time, hashlib, json
from agents.core.base_agent import BaseAgent, AgentResult

def _hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

class AuditAgent(BaseAgent):
    role = "audit"

    def run(self, **kwargs) -> AgentResult:
        entry = {
            "ts": time.time(),
            "actor": kwargs.get("actor","unknown"),
            "action": kwargs.get("action","noop"),
            "input": kwargs.get("input",""),
            "output": kwargs.get("output",""),
            "prev_hash": kwargs.get("prev_hash",""),
        }
        entry["hash"] = _hash(json.dumps(entry, sort_keys=True) + entry["prev_hash"])
        # TODO: persist in DB table (provenance_log)
        return AgentResult(ok=True, data={"entry": entry})

