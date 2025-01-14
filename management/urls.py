from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="management_index"),
    path("analytics/home/", views.analytics_home, name="analytics_home"),
]
