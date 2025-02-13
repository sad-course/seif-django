from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import LoginForm, SignupForm

# Create your views here.


def profile(request):
    return render(request, "accounts/profile.html")


def login(request):

    if request.method == "GET":
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        email = data["email"]
        password = data["password"]
        user = {email, password}
        return HttpResponse(user)

    return render(request, "accounts/login.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            # name = data["name"]
            # email = data["email"]
            # password = data["password"]
            # phone = data["phone"]
            # cpf = data["cpf"]
            # aqui cria o usuario
            return HttpResponseRedirect(reverse_lazy("login"))
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def request_reset_password(request):
    return render(request, "accounts/request_reset_password.html")


def reset_password(request):
    return render(request, "accounts/reset_password.html")


def my_certificates(request):
    return render(request, "accounts/my_certificates.html")


def my_events(request):
    return render(request, "accounts/my_events.html")
