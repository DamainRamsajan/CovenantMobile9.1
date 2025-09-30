# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "mime_type", "created_at", "updated_at")
    search_fields = ("title", "content", "source_path")
    list_filter = ("mime_type",)
    ordering = ("-updated_at",)

