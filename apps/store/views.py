from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import Document

def index(request):
    docs = Document.objects.order_by("-created_at")[:100]
    return render(request, "store/index.html", {"docs": docs})

def ingest(request):
    if request.method == "POST":
        f = request.FILES.get("file")
        title = request.POST.get("title", "")
        if f:
            doc = Document.objects.create(title=title or f.name, file=f)
            return redirect("/store/")
    return render(request, "store/ingest.html")
