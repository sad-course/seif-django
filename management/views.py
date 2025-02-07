from django.views.generic import TemplateView


# Create your views here.
class Index(TemplateView):
    template_name = "management/index.html"


class Organizers(TemplateView):
    template_name = "management/organizers.html"


class Participants(TemplateView):
    template_name = "management/participants.html"


class AnalyticsHome(TemplateView):
    template_name = "management/analytics_home.html"


class AnalyticsEventDetail(TemplateView):
    template_name = "management/analytics_event_detail.html"


class CreateEvent(TemplateView):
    template_name = "management/create_event.html"


class RequestCreateEvent(TemplateView):
    template_name = "management/request_create_event.html"


class EventPublishRequests(TemplateView):
    template_name = "management/organizer_event_submit_requests.html"


class EventPublishRequestDetail(TemplateView):
    template_name = "management/organizer_event_submit_detail.html"


class EventSubmitDashboard(TemplateView):
    template_name = "management/event_submit_dashboard.html"


class EventSubmitDetail(TemplateView):
    template_name = "management/event_submit_detail.html"
