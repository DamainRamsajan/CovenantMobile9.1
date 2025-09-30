import os, hashlib, uuid
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from store.models import Document
from django.db import transaction

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in [".txt", ".md", ".log"]:
        return path.read_text(errors="ignore")
    if suffix == ".pdf" and PdfReader:
        text = []
        reader = PdfReader(str(path))
        for page in reader.pages:
            try:
                text.append(page.extract_text() or "")
            except Exception:
                pass
        return "\n".join(text)
    # default: best effort
    try:
        return path.read_text(errors="ignore")
    except Exception:
        return ""

class Command(BaseCommand):
    help = "Ingest documents from a directory into the local store"

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True, help="Folder with docs")

    @transaction.atomic
    def handle(self, *args, **opts):
        src = Path(opts["source"]).expanduser()
        if not src.exists() or not src.is_dir():
            raise CommandError(f"Source not found or not a dir: {src}")

        count = 0
        for root, _, files in os.walk(src):
            for name in files:
                p = Path(root) / name
                if p.suffix.lower() in {".txt", ".md", ".log", ".pdf"}:
                    content = read_text(p)
                    if not content.strip():
                        continue
                    doc_id = hashlib.sha1(p.as_posix().encode()).hexdigest()[:40]
                    Document.objects.update_or_create(
                        id=doc_id,
                        defaults={
                            "title": p.name,
                            "content": content,
                            "policy_tags": "",
                        },
                    )
                    count += 1
        self.stdout.write(self.style.SUCCESS(f"Ingested/updated {count} docs from {src}"))

