from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Profile, KPI, Scorecard, Playbook
from .forms import ProfileForm, KPIForm, ScorecardForm, PlaybookForm
from .publisher import publish

def index(request):
    return render(request, "configurator/index.html", {
        "profiles": Profile.objects.order_by("name"),
        "kpis": KPI.objects.select_related("profile").order_by("profile__name","name")[:50],
        "scorecards": Scorecard.objects.select_related("profile").order_by("profile__name","name")[:50],
        "playbooks": Playbook.objects.select_related("profile").order_by("profile__name","name")[:50],
    })

# ---- Profile CRUD
def profile_new(request):
    if request.method == "POST":
        f = ProfileForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect("/configurator/")
    else:
        f = ProfileForm()
    return render(request, "configurator/profile_form.html", {"form": f})

def profile_edit(request, pk):
    obj = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        f = ProfileForm(request.POST, instance=obj)
        if f.is_valid(): f.save(); return redirect("/configurator/")
    else: f = ProfileForm(instance=obj)
    return render(request, "configurator/profile_form.html", {"form": f, "obj": obj})

# ---- KPI CRUD
def kpi_list(request):
    qs = KPI.objects.select_related("profile").order_by("profile__name","name")
    return render(request, "configurator/kpi_list.html", {"kpis": qs})

def kpi_new(request):
    if request.method == "POST":
        f = KPIForm(request.POST)
        if f.is_valid(): f.save(); return redirect("/configurator/kpis")
    else: f = KPIForm()
    return render(request, "configurator/kpi_form.html", {"form": f})

def kpi_edit(request, pk):
    obj = get_object_or_404(KPI, pk=pk)
    if request.method == "POST":
        f = KPIForm(request.POST, instance=obj)
        if f.is_valid(): f.save(); return redirect("/configurator/kpis")
    else: f = KPIForm(instance=obj)
    return render(request, "configurator/kpi_form.html", {"form": f, "obj": obj})

# ---- Scorecard
def scorecard_list(request):
    qs = Scorecard.objects.select_related("profile").order_by("profile__name","name")
    return render(request, "configurator/scorecard_list.html", {"scorecards": qs})

def scorecard_new(request):
    if request.method == "POST":
        f = ScorecardForm(request.POST)
        if f.is_valid(): f.save(); return redirect("/configurator/scorecards")
    else: f = ScorecardForm()
    return render(request, "configurator/scorecard_form.html", {"form": f})

def scorecard_edit(request, pk):
    obj = get_object_or_404(Scorecard, pk=pk)
    if request.method == "POST":
        f = ScorecardForm(request.POST, instance=obj)
        if f.is_valid(): f.save(); return redirect("/configurator/scorecards")
    else: f = ScorecardForm(instance=obj)
    return render(request, "configurator/scorecard_form.html", {"form": f, "obj": obj})

# ---- Playbook
def playbook_list(request):
    qs = Playbook.objects.select_related("profile").order_by("profile__name","name")
    return render(request, "configurator/playbook_list.html", {"playbooks": qs})

def playbook_new(request):
    if request.method == "POST":
        f = PlaybookForm(request.POST)
        if f.is_valid(): f.save(); return redirect("/configurator/playbooks")
    else: f = PlaybookForm()
    return render(request, "configurator/playbook_form.html", {"form": f})

def playbook_edit(request, pk):
    obj = get_object_or_404(Playbook, pk=pk)
    if request.method == "POST":
        f = PlaybookForm(request.POST, instance=obj)
        if f.is_valid(): f.save(); return redirect("/configurator/playbooks")
    else: f = PlaybookForm(instance=obj)
    return render(request, "configurator/playbook_form.html", {"form": f, "obj": obj})

# ---- Draft & Publish
def generate_draft(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    draft = {
        "profile": profile.name,
        "kpis": list(profile.kpis.values("name","unit","target","direction")),
        "scorecards": list(profile.scorecards.values("name","notes")),
        "playbooks": list(profile.playbooks.values("name","trigger","action")),
    }
    profile.draft_json = draft
    profile.save(update_fields=["draft_json"])
    return render(request, "configurator/draft_preview.html", {"profile": profile, "draft": draft})

def publish_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    path = publish(profile)
    return render(request, "configurator/raw.html", {"text": f"Published to {path}"})
