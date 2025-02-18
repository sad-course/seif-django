from django.views.generic import ListView, DetailView
from .models import Event


# Create your views here.
class Index(ListView):
    model = Event
    template_name = "core/index.html"
    context_object_name = "events"


class Details(DetailView):
    model = Event
    template_name = "core/event_detail.html"
    context_object_name = "event"
    pk_url_kwarg = "event_id"
