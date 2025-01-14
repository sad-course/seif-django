from django.shortcuts import render

# Create your views here.


def profile(request):
    return render(request, "accounts/profile.html")


def login(request):
    context = {}
    return render(request, "accounts/login.html", context=context)


def signup(request):
    return render(request, "accounts/signup.html")


def request_reset_password(request):
    return render(request, "accounts/request_reset_password.html")


def reset_password(request):
    return render(request, "accounts/reset_password.html")


def my_certificates(request):
    return render(request, "accounts/my_certificates.html")


def my_events(request):
    return render(request, "accounts/my_events.html")
