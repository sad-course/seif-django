from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from .forms import EventForm, EventPublishRequestForm, ActivityForm
from .models import Event, Tag, Activity, ActivityType


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


def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    # Requisição para atualizar evento
    if request.method == "POST" and "event_form" in request.POST:
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            event.title = data["title"]
            event.description = data["description"]
            event.banner = data["banner"]
            event.campus = data["campus"]
            event.status = data["initial_status"]
            event.init_date = data["init_date"]
            event.end_date = data["end_date"]
            event.save()

            tag_names = data["tags"].split(",")
            tags = []

            for tag_name in tag_names:
                tag_name = tag_name.strip()
                # pylint: disable=W0612
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)

            event.tags.set(tags)
            event.save()

            messages.success(request, "Evento criado!")
            return redirect(reverse_lazy("management"))
    else:
        form = EventForm(
            initial={
                "title": event.title,
                "description": event.description,
                "init_date": event.init_date,
                "end_date": event.end_date,
                "initial_status": event.status,
                "campus": event.campus,
            }
        )

    # Requisição para criar a atividade
    if request.POST and "activity_form" in request.POST:

        activity_form = ActivityForm(request.POST)
        if activity_form.is_valid():
            data = activity_form.cleaned_data
            new_activity = Activity.objects.create(
                title=data["title"],
                description=data["description"],
                init_date=data["init_date"],
                end_date=data["end_date"],
                instructor=data["instructor"],
                estimated_duration=data["estimated_duration"],
                capacity=data["capacity"],
                event=event,
            )
            # pylint: disable=W0612
            new_type, created = ActivityType.objects.get_or_create(name=data["type"])
            new_activity.activity_type = new_type
            new_activity.save()

            messages.success(request, "Atividade criada com sucesso!")

            return redirect(reverse_lazy("edit_event", kwargs={"event_id": event.id}))
    else:
        activity_form = ActivityForm()

    # Requisição para deletar uma atividade
    if request.POST and "activity_id" in request.POST:
        activity_id = request.POST.get("activity_id")

        activity = Activity.objects.get(id=activity_id, event=event)
        activity.delete()
        messages.success(request, "Atividade deletada com sucesso!")

        return redirect(reverse_lazy("edit_event", kwargs={"event_id": event.id}))

    return render(
        request,
        "management/edit_event.html",
        {
            "form": form,
            "event": event,
            "activity_form": activity_form,
        },
    )


class CreateEventRequestView(FormView):
    template_name = "management/request_create_event.html"
    form_class = EventPublishRequestForm

    def form_valid(self, form):
        data = form.cleaned_data

        new_event = Event.objects.create(
            title=data["event_title"],
            description=data["description"],
            campus=data["campus"],
            init_date=data["init_date"],
            end_date=data["end_date"],
            created_by=self.request.user,
        )

        messages.success(self.request, "Evento solicitado com sucesso!")
        return redirect(reverse_lazy("edit_event", kwargs={"event_id": new_event.id}))

    def form_invalid(self, form):
        messages.error(
            self.request, "Há erros no formulário. Por favor, verifique os campos."
        )
        return super().form_invalid(form)


def event_publish_requests(request):
    return render(request, "management/organizer_event_submit_requests.html")


def event_publish_request_detail(request):
    return render(request, "management/organizer_event_submit_detail.html")


def event_submit_dashboard(request):
    return render(request, "management/event_submit_dashboard.html")


def event_submit_detail(request):
    return render(request, "management/event_submit_detail.html")
