from django.contrib.auth import views as auth_views

from django.urls import path
from .views import (
    SignIn,
    SignUp,
    Profile,
    reset_password,
    request_reset_password,
    MyCertificates,
    my_events,
)

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", SignIn.as_view(), name="login"),
    path("profile/", Profile.as_view(), name="profile"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "request_reset_password/", request_reset_password, name="request_reset_password"
    ),
    path("reset_password/", reset_password, name="reset_password"),
    path("my_certificates/", MyCertificates.as_view(), name="my_certificates"),
    path("my_events/", my_events, name="my_events"),
]
