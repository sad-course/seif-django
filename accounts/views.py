from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from core.models import EventSubscription
from .forms import LoginForm, SignupForm
from .models import Participant


# Create your views here.
@method_decorator(login_required, name="dispatch")
class Profile(TemplateView):
    def get(self, *args, **kwargs):
        participant = self.request.user
        event_subscriptions = EventSubscription.objects.filter(
            participant=participant
        ).count()

        user_event_subs = {
            "event_count": event_subscriptions,
        }
        return render(self.request, "accounts/profile.html", context=user_event_subs)

    def post(self, *args, **kwargs):
        if self.request.FILES.get("photo"):
            participant = self.request.user
            participant.avatar = self.request.FILES["photo"]
            participant.save()
            return redirect("profile")

        return self.get(self.request, *args, **kwargs)


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
