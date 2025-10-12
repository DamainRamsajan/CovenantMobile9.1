from django.shortcuts import render

def kpi_dashboard(request):
    # Placeholder KPI data – this will later come from your models or JSON file
    kpis = {
        "compliance_score": 92,
        "documents_ingested": 12,
        "agents_active": 5,
        "last_run": "a2f3e89",
        "uptime": "99.7%",
    }
    return render(request, "ui/kpi.html", {"kpis": kpis})
