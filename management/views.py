from django.shortcuts import render
from django.views.generic import ListView
from .models import Participant


# Create your views here.
def index(request):
    return render(request, "management/index.html")


def organizers(request):
    return render(request, "management/organizers.html")


class Participants(ListView):
    model = Participant
    template_name = "management/participants.html"
    context_object_name = "participants"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["participants_count"] = Participant.objects.all().count()
        return context


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
