from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=120, unique=True)
    domain = models.CharField(max_length=120, blank=True, default="")
    draft_json = models.JSONField(default=dict, blank=True)
    published_version = models.CharField(max_length=50, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

class KPI(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="kpis")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")
    unit = models.CharField(max_length=32, blank=True, default="")
    target = models.FloatField(null=True, blank=True)
    direction = models.CharField(max_length=8, choices=[("up","up"),("down","down"),("range","range")], default="up")

    class Meta:
        unique_together = ("profile","name")

class Scorecard(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="scorecards")
    name = models.CharField(max_length=120)
    notes = models.TextField(blank=True, default="")

class Playbook(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="playbooks")
    name = models.CharField(max_length=120)
    trigger = models.CharField(max_length=255, blank=True, default="")
    action = models.TextField(blank=True, default="")
