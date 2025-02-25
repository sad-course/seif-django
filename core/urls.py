from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="home"),
    path("event/<int:event_id>/", views.Details.as_view(), name="event_details"),
    path(
        "event/subcription/",
        views.EventSubscriptionView.as_view(),
        name="event_subscription",
    ),
    path(
        "event/subcription/<int:event_id>/",
        views.EventSubscriptionDetailView.as_view(),
        name="event_subscription_update",
    ),
]
