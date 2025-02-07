from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="management"),
    path("organizers/", views.Organizers.as_view(), name="organizers"),
    path("participants/", views.Participants.as_view(), name="participants"),
    path("create_event/", views.CreateEvent.as_view(), name="create_event"),
    path(
        "request_create_event/",
        views.RequestCreateEvent.as_view(),
        name="request_create_event",
    ),
    path("analytics/home/", views.AnalyticsHome.as_view(), name="analytics_home"),
    path(
        "analytics/event/",
        views.AnalyticsEventDetail.as_view(),
        name="analytics_event_detail",
    ),
    path(
        "event/request/",
        views.EventPublishRequests.as_view(),
        name="event_publish_request",
    ),
    path(
        "event/request/detail/",
        views.EventPublishRequestDetail.as_view(),
        name="event_request_detail",
    ),
    path(
        "event/submit/",
        views.EventSubmitDashboard.as_view(),
        name="event_submit_dashboard",
    ),
    path(
        "event/submit/detail/",
        views.EventSubmitDetail.as_view(),
        name="event_submit_detail",
    ),
]
