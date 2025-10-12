from django.shortcuts import render

def configurator(request):
    models = [
        {"name": "TinyLlama", "status": "Active"},
        {"name": "Mistral-7B", "status": "Idle"},
        {"name": "Phi-2", "status": "Available"}
    ]
    return render(request, "ui/configurator.html", {"models": models})

