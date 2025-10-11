from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services.llm_client import complete
import json

def llm_ping(request):
    reply = complete("pong")
    return JsonResponse({"ok": reply.strip().lower().startswith("pong"), "reply": reply})

@csrf_exempt
def chat(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8") or "{}")
        prompt = body.get("prompt") or ""
    else:
        prompt = request.GET.get("q", "")
    if not prompt:
        return JsonResponse({"error": "missing prompt"}, status=400)
    reply = complete(prompt, 128)
    return JsonResponse({"prompt": prompt, "reply": reply})
