from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from apps.providers.llama_engine import chat_complete

SYSTEM_PROMPT = "You are Covenant, a helpful on-device assistant. Be concise and accurate."

def qa_form(request):
    return render(request, "workflows/qa.html", {"answer": None})

@require_POST
def qa(request):
    q = request.POST.get("q", "").strip()
    if not q:
        return JsonResponse({"ok": False, "error": "Empty question"}, status=400)
    answer = chat_complete(SYSTEM_PROMPT, q, temperature=0.2, max_tokens=400)
    return JsonResponse({"ok": True, "answer": answer})
