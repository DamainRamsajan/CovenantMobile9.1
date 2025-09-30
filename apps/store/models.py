# -*- coding: utf-8 -*-
"""
Covenant Mobile v9.1 — apps/store/models.py
Minimal store models for offline RAG. Extend later with Vector, ProvenanceLog, PolicyBundle.
"""
from __future__ import annotations
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    source_path = models.CharField(max_length=1024, blank=True, default="")
    mime_type = models.CharField(max_length=50, blank=True, default="")
    policy_tags = models.CharField(max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["mime_type"]),
        ]
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.title[:80]} ({self.mime_type})"

# Placeholders for future phases (leave commented until we implement):
# class Vector(models.Model):
#     doc = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="vectors")
#     dim = models.IntegerField(default=768)
#     model = models.CharField(max_length=100, default="gte-small")
#     embedding = models.BinaryField()  # or JSON/Text in first pass
#     created_at = models.DateTimeField(auto_now_add=True)
#
# class ProvenanceLog(models.Model):
#     run_id = models.CharField(max_length=64)
#     step_no = models.IntegerField()
#     actor = models.CharField(max_length=80)
#     action = models.CharField(max_length=120)
#     input_hash = models.CharField(max_length=64, blank=True, default="")
#     output_hash = models.CharField(max_length=64, blank=True, default="")
#     policy_decision = models.CharField(max_length=80, blank=True, default="")
#     ts = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         unique_together = ("run_id","step_no")
