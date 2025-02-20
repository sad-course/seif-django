from django.shortcuts import render
from django.views.generic import ListView
from .models import Event


def index(request):
    return render(request, "management/index.html")


# Create your views here.
class IndexListView(ListView):
    model = Event
    template_name = "management/index.html"
    context_object_name = "events"
    paginate_by = 10  # Número de eventos por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events_count"] = Event.objects.count()
        return context


def organizers(request):
    return render(request, "management/organizers.html")


def participants(request):
    return render(request, "management/participants.html")


def analytics_home(request):
    return render(request, "management/analytics_home.html")


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
