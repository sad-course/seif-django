from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Count
from .models import Event, Participant, Activity


events = Event.objects.annotate(total_activities=Count("activity"))


# Create your views here.
class Index(ListView):
    model = Event
    template_name = "management/index.html"
    context_object_name = "events"
    paginate_by = 10  # Número de eventos por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events_count"] = Event.objects.count()
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


def participants(request):
    return render(request, "management/participants.html")


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


def create_event(request):
    return render(request, "management/create_event.html")


def request_create_event(request):
    return render(request, "management/request_create_event.html")


def event_publish_requests(request):
    return render(request, "management/organizer_event_submit_requests.html")


def event_publish_request_detail(request):
    return render(request, "management/organizer_event_submit_detail.html")


def event_submit_dashboard(request):
    return render(request, "management/event_submit_dashboard.html")


def event_submit_detail(request):
    return render(request, "management/event_submit_detail.html")
