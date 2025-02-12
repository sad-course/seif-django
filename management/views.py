from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import EventForm, EventPublishRequestForm, ActivityForm


# Create your views here.
def index(request):
    return render(request, "management/index.html")


def organizers(request):
    return render(request, "management/organizers.html")


def participants(request):
    return render(request, "management/participants.html")


def analytics_home(request):
    return render(request, "management/analytics_home.html")


def analytics_event_detail(request):
    return render(request, "management/analytics_event_detail.html")


def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        activity_form = ActivityForm(request.POST)
        if form.is_valid() and activity_form.is_valid():
            # titulo = form.cleaned_data["titulo"]
            # descricao = form.cleaned_data["descricao"]
            # imagem = form.cleaned_data["imagem"]
            # inicio = form.cleaned_data["inicio"]
            # fim = form.cleaned_data["fim"]
            # horario_inicio = form.cleaned_data["horario_inicio"]
            # status_inicial = form.cleaned_data["status_inicial"]
            # tags = form.cleaned_data["tags"]
            # campus = form.cleaned_data["campus"]
            # organizadores = form.cleaned_data["organizadores"]
            print(form.cleaned_data)
            print(activity_form.cleaned_data)
            return HttpResponseRedirect(reverse_lazy("management"))
    else:
        form = EventForm()
        activity_form = ActivityForm()

    return render(
        request,
        "management/create_event.html",
        {
            "form": form,
            "activity_form": activity_form,
        },
    )


def request_create_event(request):
    if request.method == "POST":
        form = EventPublishRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # dados
            print(form.cleaned_data)
            return redirect(reverse_lazy("management"))
    else:
        form = EventPublishRequestForm()

    return render(request, "management/request_create_event.html", {"form": form})


def event_publish_requests(request):
    return render(request, "management/organizer_event_submit_requests.html")


def event_publish_request_detail(request):
    return render(request, "management/organizer_event_submit_detail.html")


def event_submit_dashboard(request):
    return render(request, "management/event_submit_dashboard.html")


def event_submit_detail(request):
    return render(request, "management/event_submit_detail.html")
