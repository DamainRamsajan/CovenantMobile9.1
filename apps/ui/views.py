from django.shortcuts import render

def home(request):
    return render(request, "ui/home.html")

def kpi_dashboard(request):
    return render(request, "ui/kpi.html")

def configurator_home(request):
    return render(request, "ui/configurator.html")

