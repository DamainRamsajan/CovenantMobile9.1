from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="store_index"),
    path("ingest", views.ingest, name="store_ingest"),
]
