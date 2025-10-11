from django.http import JsonResponse
from .llama_engine import health as engine_health

def health(request):
    return JsonResponse(engine_health(), safe=False)
