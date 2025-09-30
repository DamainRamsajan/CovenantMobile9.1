# -*- coding: utf-8 -*-
"""
QueryAgent: retrieves top-k candidate chunks and builds an answer draft prompt.
Note: generation is handled by provider (HttpLLM) or ICE wrapper.
"""
from __future__ import annotations
from typing import Dict, Any
from dataclasses import dataclass
from agents.core.base_agent import BaseAgent, AgentResult
from core.retriever import retrieve

@dataclass
class QueryConfig:
    top_k: int = 5

class QueryAgent(BaseAgent):
    role = "query"

    def run(self, **kwargs) -> AgentResult:
        question = (kwargs.get("question") or "").strip()
        if not question:
            return AgentResult(ok=False, error="empty question")
        cfg = QueryConfig(top_k=int(kwargs.get("top_k", self.config.get("top_k", 5))))

        hits = retrieve(question, top_k=cfg.top_k)
        context = "\n\n".join(
            f"[{i+1}] {d.title}\n{(d.content or '')[:800]}"
            for i, (d, _) in enumerate(hits)
        )
        prompt = (
            "You are Covenant. Answer using ONLY the context below. "
            "If the answer is not present, say you don't know.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        citations = [{"title": d.title, "path": d.source_path} for d, _ in hits]
        return AgentResult(ok=True, data={"prompt": prompt, "citations": citations, "n_hits": len(hits)})

