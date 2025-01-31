from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("details", views.details, name="event_details"),
]
