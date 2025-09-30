# -*- coding: utf-8 -*-
"""
IngestorAgent: scan a path for txt/md/pdf and persist to Document.
"""
from __future__ import annotations
from typing import Dict, Any, List
from pathlib import Path
from dataclasses import dataclass
from django.conf import settings
from apps.store.models import Document
from agents.core.base_agent import BaseAgent, AgentResult

@dataclass
class IngestConfig:
    path: str
    include_ext: List[str] = (".txt", ".md", ".pdf")

class IngestorAgent(BaseAgent):
    role = "ingestor"

    def run(self, **kwargs) -> AgentResult:
        cfg = IngestConfig(
            path=kwargs.get("path") or self.config.get("path") or settings.DOCS_PATH,
            include_ext=list(kwargs.get("include_ext", (".txt",".md",".pdf")))
        )
        base = Path(cfg.path).expanduser()
        if not base.exists():
            return AgentResult(ok=False, error=f"path not found: {base}")

        count = 0
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in cfg.include_ext:
                continue
            text = self._read(p)
            if not text.strip():
                continue
            title = p.stem.replace("_"," ").strip()[:300]
            Document.objects.update_or_create(
                source_path=str(p),
                defaults={
                    "title": title,
                    "content": text,
                    "mime_type": p.suffix.lower().lstrip("."),
                },
            )
            count += 1
        return AgentResult(ok=True, data={"ingested": count, "path": str(base)})

    def _read(self, p: Path) -> str:
        if p.suffix.lower() in {".txt",".md"}:
            return p.read_text(encoding="utf-8", errors="ignore")
        if p.suffix.lower() == ".pdf":
            try:
                from pypdf import PdfReader
                return "\n".join(page.extract_text() or "" for page in PdfReader(str(p)).pages)
            except Exception:
                return ""
        return ""

