from django.views.generic import ListView, DetailView
from django.core.serializers import serialize
from django.shortcuts import render
from .models import Event
from .filters import EventFilter


filtered_choices = Event.EventStatus.choices[1], Event.EventStatus.choices[2]


# Create your views here.
class Index(ListView):
    model = Event
    template_name = "core/index.html"
    context_object_name = "events"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()

        event_filter = EventFilter(self.request.GET, queryset=queryset)

        return event_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filter"] = EventFilter(self.request.GET, queryset=self.get_queryset())
        context["status_choices"] = filtered_choices
        context["campus_choices"] = Event.Campus.choices
        return context

    def get_events(self, request):
        events = Event.objects.all()
        page_number = request.GET("page")
        page_obj = serialize("python", (page_number))
        context = {"events": events, "page_obj": page_obj}
        return render(request, "home", context)


class Details(DetailView):
    model = Event
    template_name = "core/event_detail.html"
    context_object_name = "event"
    pk_url_kwarg = "event_id"
