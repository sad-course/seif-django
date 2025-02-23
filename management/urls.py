from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="management"),
    path("organizers/", views.Organizers.as_view(), name="organizers"),
    path("participants/", views.Participants.as_view(), name="participants"),
    path("edit_event/<int:event_id>/", views.edit_event, name="edit_event"),
    path(
        "request_create_event/",
        views.CreateEventRequestView.as_view(),
        name="request_create_event",
    ),
    path("analytics/home/", views.AnalyticsHome.as_view(), name="analytics_home"),
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
    path(
        "event/submit/detail/", views.event_submit_detail, name="event_submit_detail"
    ),  # esse aqui
    path("tags/", views.TagsListView.as_view(), name="get_tags_json"),
]
