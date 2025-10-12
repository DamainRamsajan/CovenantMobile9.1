from django.urls import path
from . import views
from . import views_chat

urlpatterns = [
    path("", views.home, name="home"),
    path("chat/", views_chat.chat_page, name="chat"),
    path("chat/api/", views_chat.chat_api, name="chat_api"),
    path("kpi/", views.kpi_dashboard, name="kpi"),
    path("configurator/", views.configurator_home, name="configurator"),
]
