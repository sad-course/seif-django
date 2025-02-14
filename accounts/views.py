from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .forms import LoginForm, SignupForm
from .models import Participant

# Create your views here.


def profile(request):
    return render(request, "accounts/profile.html")


class SignIn(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        data = form.cleaned_data
        email = data["email"]
        password = data["password"]

        user = authenticate(self.request, email=email, password=password)
        if user is None:
            form.add_error(None, "Email ou senha incorreta")
            return self.form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SignUp(FormView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = Participant()
        data = form.cleaned_data
        user.username = data["name"]
        user.email = data["email"]
        user.phone = data["phone"]
        user.cpf = data["cpf"]
        user.set_password(data["password"])

        already_exists_user = Participant.objects.filter(email=user.email).exists()
        if already_exists_user:
            form.add_error(None, "Email já cadastrado")
            return self.form_invalid(form)

        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


def request_reset_password(request):
    return render(request, "accounts/request_reset_password.html")


def reset_password(request):
    return render(request, "accounts/reset_password.html")


def my_certificates(request):
    return render(request, "accounts/my_certificates.html")


def my_events(request):
    return render(request, "accounts/my_events.html")
