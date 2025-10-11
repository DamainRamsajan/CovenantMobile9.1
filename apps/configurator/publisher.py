import json, os, time, pathlib
from django.conf import settings

BASE = pathlib.Path(settings.BASE_DIR) if hasattr(settings, "BASE_DIR") else pathlib.Path(".")
PROFILES_DIR = BASE / "data" / "profiles" / "default"

def publish(profile, version: str = None):
    version = version or f"v{time.strftime('%Y.%m.%d.%H%M')}"
    target = PROFILES_DIR / version
    target.mkdir(parents=True, exist_ok=True)

    domain = {"name": profile.domain or "default", "profile": profile.name}
    scorecards = [{"name": s.name, "notes": s.notes} for s in profile.scorecards.all()]
    playbooks = [{"name": p.name, "trigger": p.trigger, "action": p.action} for p in profile.playbooks.all()]
    kpis = [{"name": k.name, "unit": k.unit, "target": k.target, "direction": k.direction,
             "description": k.description} for k in profile.kpis.all()]

    (target / "domain.yaml").write_text(json.dumps(domain, indent=2))
    (target / "scorecards.yaml").write_text(json.dumps(scorecards, indent=2))
    (target / "playbooks.yaml").write_text(json.dumps(playbooks, indent=2))
    (target / "policy.bundle").write_text("{}")
    active = PROFILES_DIR / "active"
    if active.exists() or active.is_symlink():
        active.unlink()
    active.symlink_to(version)
    profile.published_version = version
    profile.save(update_fields=["published_version"])
    return str(target)
