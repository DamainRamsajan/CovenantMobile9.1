from django import forms
from .models import Profile, KPI, Scorecard, Playbook

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["name","domain"]

class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ["profile","name","description","unit","target","direction"]

class ScorecardForm(forms.ModelForm):
    class Meta:
        model = Scorecard
        fields = ["profile","name","notes"]

class PlaybookForm(forms.ModelForm):
    class Meta:
        model = Playbook
        fields = ["profile","name","trigger","action"]
