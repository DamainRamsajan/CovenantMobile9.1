from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "ui/home.html", {"title": "Covenant Mobile"})

def settings_view(request):
    return render(request, "ui/settings.html", {})

def diagnostics(request):
    return render(request, "ui/diagnostics.html", {})
