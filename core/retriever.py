# -*- coding: utf-8 -*-
"""
Covenant Mobile v9.1 — core/retriever.py
Deterministic, dependency-light retriever over Document rows.
Upgrade path: FTS5 + sqlite-vec re-rank.
"""
from __future__ import annotations
from typing import List, Tuple
from apps.store.models import Document

def retrieve(query: str, top_k: int = 5) -> List[Tuple[Document, int]]:
    q = (query or "").lower().strip()
    if not q:
        return []
    tokens = [t for t in q.split() if t]
    scored: list[tuple[Document,int]] = []
    # naive scoring: term counts in title+content
    for d in Document.objects.all().only("id","title","content","source_path"):
        text = f"{d.title}\n{d.content}".lower()
        score = sum(text.count(tok) for tok in tokens[:6])
        if score > 0:
            scored.append((d, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:max(1, top_k)]

