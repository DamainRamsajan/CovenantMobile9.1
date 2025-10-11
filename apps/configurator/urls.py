from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="configurator_index"),
    path("profiles/new", views.profile_new, name="profile_new"),
    path("profiles/<int:pk>/edit", views.profile_edit, name="profile_edit"),

    path("kpis", views.kpi_list, name="kpi_list"),
    path("kpis/new", views.kpi_new, name="kpi_new"),
    path("kpis/<int:pk>/edit", views.kpi_edit, name="kpi_edit"),

    path("scorecards", views.scorecard_list, name="scorecard_list"),
    path("scorecards/new", views.scorecard_new, name="scorecard_new"),
    path("scorecards/<int:pk>/edit", views.scorecard_edit, name="scorecard_edit"),

    path("playbooks", views.playbook_list, name="playbook_list"),
    path("playbooks/new", views.playbook_new, name="playbook_new"),
    path("playbooks/<int:pk>/edit", views.playbook_edit, name="playbook_edit"),

    path("profiles/<int:profile_id>/draft", views.generate_draft, name="generate_draft"),
    path("profiles/<int:profile_id>/publish", views.publish_profile, name="publish_profile"),
]
