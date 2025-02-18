from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="management"),
    path("organizers/", views.organizers, name="organizers"),
    path("participants/", views.Participants.as_view(), name="participants"),
    path("create_event/", views.create_event, name="create_event"),
    path(
        "request_create_event/", views.request_create_event, name="request_create_event"
    ),
    path("analytics/home/", views.analytics_home, name="analytics_home"),
    path(
        "analytics/event/", views.analytics_event_detail, name="analytics_event_detail"
    ),
    path("event/request/", views.event_publish_requests, name="event_publish_request"),
    path(
        "event/request/detail/",
        views.event_publish_request_detail,
        name="event_request_detail",
    ),
    path("event/submit/", views.event_submit_dashboard, name="event_submit_dashboard"),
    path("event/submit/detail/", views.event_submit_detail, name="event_submit_detail"),
]
