from django.shortcuts import render
from django.http import JsonResponse

def chat_page(request):
    return render(request, "ui/chat.html")

def chat_api(request):
    # Placeholder response for now
    data = {"response": "Chat API is running!"}
    return JsonResponse(data)
