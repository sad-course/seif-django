from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.views.generic import FormView, ListView, DetailView
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Count

from .filters import EventFilter
from .forms import EventForm, EventPublishRequestForm, ActivityForm
from .models import Event, Tag, Activity, ActivityType, Participant


events = Event.objects.annotate(total_activities=Count("activity"))


# Create your views here.
class Index(ListView):
    model = Event
    template_name = "management/index.html"
    context_object_name = "events"
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.all()
        event_filter = EventFilter(self.request.GET, queryset=queryset)
        return event_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events_count"] = Event.objects.count()
        context["organizers_count"] = (
            Participant.objects.filter(event__status__in=["active", "approved"])
            .distinct()
            .count()
        )
        context["total_activities"] = Activity.objects.count()
        context["filter"] = EventFilter(self.request.GET)
        return context


class Organizers(ListView):
    model = Participant
    template_name = "management/organizers.html"
    context_object_name = "organizers"
    paginate_by = 10

    def get_queryset(self):
        return Participant.objects.filter(
            event__status__in=["active", "approved"]
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organizers_count"] = self.get_queryset().count()
        return context


class Participants(ListView):
    model = Participant
    template_name = "management/participants.html"
    context_object_name = "participants"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participants_count"] = Participant.objects.all().count()
        return context


class AnalyticsHome(ListView):
    model = Event
    template_name = "management/analytics_home.html"
    context_object_name = "events"
    paginate_by = 10

    def get_queryset(self):
        return Event.objects.annotate(total_activities=Count("activity"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_events"] = Event.objects.count()
        context["total_participants"] = Participant.objects.count()
        context["total_activities"] = Activity.objects.count()  # Contagem de atividades
        active_events = Event.objects.filter(status="active").count()
        context["active_events_percentage"] = (
            (active_events / context["total_events"]) * 100
            if context["total_events"]
            else 0
        )

        return context


def analytics_event_detail(request):
    return render(request, "management/analytics_event_detail.html")


def edit_event(request, event_id):  # pylint: disable=R0915
    event = Event.objects.get(id=event_id)
    tags = list(event.tags.all().only("name").values_list("name", flat=True))
    tags_into_string = ",".join(tag for tag in tags)

    event_initial_data = {
        "title": event.title,
        "description": event.description,
        "init_date": event.init_date.date(),
        "end_date": event.end_date.date(),
        "status": event.status,
        "campus": event.campus,
        "tags": tags_into_string,
        "organizers": event.organizers.all(),
    }
    # Requisição para atualizar evento
    if request.method == "POST" and "event_form" in request.POST:
        form = EventForm(request.POST, request.FILES, initial=event_initial_data)
        if form.is_valid():
            data = form.cleaned_data
            event.title = data["title"]
            event.description = data["description"]
            event.campus = data["campus"]
            event.status = data["status"]
            event.init_date = data["init_date"]
            event.end_date = data["end_date"]
            if data["banner"]:
                event.banner = data["banner"]
            event.save()

            tag_names = data["tags"].split(",")
            tags = []

            for tag_name in tag_names:
                tag_name = tag_name.strip()
                # pylint: disable=W0612
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)

            event.tags.set(tags)

            selected_organizers = form.cleaned_data["organizers"]
            organizer_ids = selected_organizers.values_list("id", flat=True)

            event.organizers.set(organizer_ids)

            # tornando os participantes selecionados em organizadores
            for organizer in organizer_ids:
                participant = Participant.objects.get(id=organizer)
                group = Group.objects.get(name="Organizers")
                participant.groups.add(group)
                participant.save()

            event.save()

            messages.success(request, "Evento criado!")
            return redirect(reverse_lazy("management"))
    else:
        form = EventForm(initial=event_initial_data)

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

            activity_type = ActivityType.objects.get(id=data["activity_type"])
            new_activity.activity_type = activity_type
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

        group = Group.objects.get(name="Organizers")
        self.request.user.groups.add(group)
        self.request.user.save()

        messages.success(self.request, "Evento solicitado com sucesso!")
        return redirect(reverse_lazy("edit_event", kwargs={"event_id": new_event.id}))

    def form_invalid(self, form):
        messages.error(
            self.request, "Há erros no formulário. Por favor, verifique os campos."
        )
        return super().form_invalid(form)


class EventPublishRequests(ListView):
    model = Event
    template_name = "management/organizer_event_submit_requests.html"
    context_object_name = "draft_events"

    def get_queryset(self):
        return Event.objects.filter(status=Event.EventStatus.DRAFT)


def event_publish_request_detail(request):
    return render(request, "management/organizer_event_submit_detail.html")


def event_submit_dashboard(request):
    return render(request, "management/event_submit_dashboard.html")


class EventSubmitDetail(DetailView):
    model = Event
    template_name = "management/event_submit_detail.html"
    context_object_name = "event"

    def post(self, request, pk, *args, **kwargs):
        event = get_object_or_404(Event, pk=pk)
        if "approve" in request.POST:
            event.status = Event.EventStatus.APPROVED
            event.save()
            messages.success(request, "Evento aprovado!")
        elif "reject" in request.POST:
            event.status = Event.EventStatus.RECUSED  # Alterado para RECUSED
            event.save()
            messages.success(request, "Evento recusado!")
        return redirect(reverse_lazy("event_submit_detail", kwargs={"pk": pk}))


class TagsListView(View):
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all().values_list("name", flat=True)

        return JsonResponse(list(tags), safe=False)
