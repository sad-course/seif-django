from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="management"),
    path("organizers/", views.organizers, name="organizers"),
    path("participants/", views.participants, name="participants"),
    path("create_event/", views.create_event, name="create_event"),
    path(
        "request_create_event/", views.request_create_event, name="request_create_event"
    ),
    path("analytics/home/", views.analytics_home, name="analytics_home"),
    path(
        "analytics/event/", views.analytics_event_detail, name="analytics_event_detail"
    ),
]
