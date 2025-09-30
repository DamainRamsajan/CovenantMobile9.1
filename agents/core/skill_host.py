# -*- coding: utf-8 -*-
"""
Covenant Mobile v9.1 — agents/core/skill_host.py
SkillHost placeholder: declare/run tools with minimal surface.
"""
from __future__ import annotations
from typing import Dict, Callable, Any

class SkillHost:
    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]) -> None:
        self._tools[name] = fn

    def run(self, name: str, **kwargs) -> Any:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name](**kwargs)

