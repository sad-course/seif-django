from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="management"),
    path("organizers/", views.organizers, name="organizers"),
    path("participants/", views.participants, name="participants"),
    path("analytics/home/", views.analytics_home, name="analytics_home"),
    path(
        "analytics/event/", views.analytics_event_detail, name="analytics_event_detail"
    ),
    path("event/request/", views.event_publish_request, name="event_publish_request"),
]
