# -*- coding: utf-8 -*-
"""
LLMProvider interface for Covenant Mobile.
Concrete implementations must implement generate() and may implement health().
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kw) -> str:
        """Return a text completion given a prompt."""
        raise NotImplementedError

    def health(self) -> Dict[str, Any]:
        """Optional health info for diagnostics UI."""
        return {"ok": True, "provider": self.__class__.__name__}

