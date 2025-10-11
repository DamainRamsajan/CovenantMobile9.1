from django.urls import path
from . import views
urlpatterns = [
    path("qa_form", views.qa_form, name="qa_form"),
    path("qa", views.qa, name="qa"),
]
