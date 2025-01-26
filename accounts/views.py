from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateUser
from .models import Participant

# Create your views here.


def profile(request):
    return render(request, "accounts/profile.html")


def login(request):
    context = {}
    return render(request, "accounts/login.html", context=context)


def signup(request):
    if request.method == "POST":
        form = CreateUser(request.POST)
        new_participant = Participant()
        if form.is_valid():
            data = form.cleaned_data

            new_participant.name = data["name"]
            new_participant.email = data["email"]
            new_participant.password = data["password"]
            new_participant.phone = data["phone"]
            new_participant.cpf = data["cpf"]

            new_participant.save()
            return HttpResponse("deu cecrto")

    form = CreateUser()
    return render(request, "accounts/signup.html", {"form": form})


def request_reset_password(request):
    return render(request, "accounts/request_reset_password.html")


def reset_password(request):
    return render(request, "accounts/reset_password.html")


def my_certificates(request):
    return render(request, "accounts/my_certificates.html")


def my_events(request):
    return render(request, "accounts/my_events.html")
