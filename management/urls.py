from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="management"),
    path("analytics/home/", views.analytics_home, name="analytics_home"),
    path("organizers/", views.organizers, name="organizers"),
    path("participants/", views.participants, name="participants"),
]
