import io
import os

from social_django.models import UserSocialAuth

from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files import File
from django.views.generic import FormView, TemplateView, ListView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from core.models import EventSubscription
from management.models import Certificate
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

        is_suap_user = UserSocialAuth.objects.filter(
            user=participant, provider="suap"
        ).first()
        context = {
            "avatar": participant.avatar,
            "event_count": event_subscriptions,
            "is_suap_user": is_suap_user,
        }

        return render(self.request, "accounts/profile.html", context=context)

    def post(self, *args, **kwargs):
        if self.request.FILES.get("photo"):
            participant = self.request.user
            participant.avatar = self.request.FILES["photo"]
            participant.save(update_fields=["avatar"])
            return redirect("profile")

        return self.get(self.request, *args, **kwargs)


class SignIn(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

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


class MyCertificates(ListView):
    model = Certificate
    template_name = "accounts/my_certificates.html"
    context_object_name = "certificates"

    def get_queryset(self):
        return Certificate.objects.filter(participant=self.request.user)


def create_certificate(participant_username, activity_title):
    # Caminho da imagem de fundo no static
    static_bg_path = finders.find("img/certificatebg.png")

    if not static_bg_path:
        raise FileNotFoundError("Imagem de fundo não encontrada no diretório static.")

    img = Image.open(static_bg_path)
    d = ImageDraw.Draw(img)

    # caminho que será salva
    media_cert_path = os.path.join(
        settings.MEDIA_ROOT, "certificates", "certificate_image.jpg"
    )
    font_path = os.path.join(
        settings.BASE_DIR, "accounts/static/fonts/BebasNeue-Regular.ttf"
    )
    font_username = os.path.join(settings.BASE_DIR, "accounts/static/fonts/shine.ttf")

    font = ImageFont.truetype(font_path, 60)
    font_user = ImageFont.truetype(font_username, 100)

    d.text((900, 500), f"{participant_username}", font=font_user, fill=(0, 0, 0))
    d.text((700, 750), f"Atividade: {activity_title}", font=font, fill=(0, 0, 0))

    # Salvar a imagem em um objeto BytesIO
    img_io = io.BytesIO()
    img.save(img_io, "JPEG")
    img_io.seek(0)

    # Cria um objeto File com a imagem gerada (sem salvar fisicamente no disco)
    image_file = File(img_io, name="certificate_image.jpg")

    # Opcionalmente, se quiser salvar a imagem diretamente em um campo do modelo ou algo similar
    # Salvar a imagem no sistema de arquivos (mídia)
    with open(media_cert_path, "wb") as f:
        f.write(img_io.getvalue())

    return image_file


class MyEvents(ListView):
    model = EventSubscription
    template_name = "accounts/my_events.html"
    context_object_name = "event_subscriptions"

    def get_queryset(self):
        return EventSubscription.objects.filter(
            participant=self.request.user, is_subcription_canceled=False
        )
