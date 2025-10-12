from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from importlib import import_module

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Root -> UI app
    path("", include("apps.ui.urls")),
]

# Optional app mounts: only add if the app's urls module exists
_optional_apps = [
    ("store/",        "apps.store.urls"),
    ("workflows/",    "apps.workflows.urls"),
    ("providers/",    "apps.providers.urls"),
    ("configurator/", "apps.configurator.urls"),
]

for prefix, dotted in _optional_apps:
    try:
        import_module(dotted)
    except Exception:
        # App not present (or urls not defined) — skip without breaking the project
        continue
    else:
        urlpatterns.append(path(prefix, include(dotted)))

# Serve media/static in dev (safe with runserver)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
