from django.urls import path
from .views import (
    SignIn,
    SignUp,
    profile,
    reset_password,
    request_reset_password,
    my_certificates,
    my_events,
)

urlpatterns = [
    path("login/", SignIn.as_view(), name="login"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("profile/", profile, name="profile"),
    path(
        "request_reset_password/", request_reset_password, name="request_reset_password"
    ),
    path("reset_password/", reset_password, name="reset_password"),
    path("my_certificates/", my_certificates, name="my_certificates"),
    path("my_events/", my_events, name="my_events"),
]
