# -*- coding: utf-8 -*-
"""
Covenant Mobile v9.1 — core/ice.py

ICE (Intelligent Coordinator Engine)
- Owns the high-level "run" lifecycle
- Talks to the EventBus
- Calls role agents (query, ingestor, compliance, audit)
- Returns a structured result for the UI

Design: simple, synchronous entrypoints with optional async via bus.enqueue later.
"""

from __future__ import annotations
from typing import Dict, Any, List
import logging
from dataclasses import dataclass, field
from core.event_bus import bus
from core.retriever import retrieve
from providers.http_llm import HttpLLM

logger = logging.getLogger(__name__)

@dataclass
class RunResult:
    ok: bool
    answer: str = ""
    citations: List[Dict[str, str]] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    error: str = ""

class ICE:
    """
    Minimal orchestrator facade. Evolve to graph-based workflows later.
    """

    def __init__(self):
        self.llm = HttpLLM()

    # ---- public API --------------------------------------------------------

    def run_query(self, question: str, top_k: int = 5) -> RunResult:
        """
        End-to-end query against local store with LLM composition.
        Emits events for observability and future subscribers.
        """
        run_meta = {"question": question, "top_k": top_k}
        bus.publish("run.started", {"stage": "query"}, meta=run_meta)

        try:
            hits = retrieve(question, top_k=top_k)
            bus.publish("retrieve.done", {"n_hits": len(hits)} , meta=run_meta)

            context = "\n\n".join(
                f"[{i+1}] {d.title}\n{(d.content or '')[:800]}"
                for i, (d, _) in enumerate(hits)
            )
            prompt = (
                "You are Covenant. Answer using ONLY the context below. "
                "If the answer is not present, say you don't know.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {question}\nAnswer:"
            )

            text = self.llm.generate(prompt, max_tokens=600)
            citations = [{"title": d.title, "path": d.source_path} for d, _ in hits]

            res = RunResult(ok=True, answer=text, citations=citations, meta={"n_hits": len(hits)})
            bus.publish("run.completed", {"status": "ok"}, meta={**run_meta, "n_hits": len(hits)})
            return res

        except Exception as e:
            logger.exception("run_query failed: %s", e)
            bus.publish("run.completed", {"status": "error", "error": str(e)}, meta=run_meta)
            return RunResult(ok=False, error=str(e))

    def ingest_path(self, path: str) -> RunResult:
        """
        Thin façade — shells out to Django mgmt command via subprocess later.
        Here we simply emit an event; UI should call the management command.
        """
        bus.publish("ingest.requested", {"path": path})
        return RunResult(ok=True, answer=f"Ingestion requested for: {path}")

# Singleton orchestrator
ice = ICE()

