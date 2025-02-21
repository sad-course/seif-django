from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="home"),
    path("event/<int:event_id>/", views.Details.as_view(), name="event_details"),
]
