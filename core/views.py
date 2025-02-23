import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from core.models import EventSubscription
from management.models import Activity, Event
from .filters import EventFilter

filtered_choices = Event.EventStatus.choices[1], Event.EventStatus.choices[2]
filtered_campus = Event.Campus.choices[1:]


# Create your views here.
class Index(ListView):
    model = Event
    template_name = "core/index.html"
    context_object_name = "events"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(
            Q(status__in=["draft", "approved", "pending"]) | Q(campus="null")
        )
        print(queryset)
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        event_filter = EventFilter(self.request.GET, queryset=queryset)
        queryset = event_filter.qs

        queryset = queryset.order_by("id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["filter"] = EventFilter(self.request.GET, queryset=queryset)
        context["status_choices"] = filtered_choices
        context["campus_choices"] = filtered_campus
        context["page_obj"] = page_obj

        # exibição do número de páginas
        num_pages = paginator.num_pages
        current_page = page_obj.number

        if num_pages <= 3:
            page_range = list(range(1, num_pages + 1))
        else:
            start_page = max(1, current_page - 1)
            end_page = min(num_pages, current_page + 1)
            page_range = list(range(start_page, end_page + 1))

            # Adiciona reticências se necessário
            if start_page > 1:
                page_range.insert(0, 1)
                if start_page > 2:
                    page_range.insert(1, None)

            if end_page < num_pages:
                if end_page < num_pages - 1:
                    page_range.append(None)
                page_range.append(num_pages)

        context["page_range"] = page_range
        return context


class Details(DetailView):
    model = Event
    template_name = "core/event_detail.html"
    context_object_name = "event"
    pk_url_kwarg = "event_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        event_id = context["event"]
        if self.request.user.is_authenticated:
            is_subscribed = EventSubscription.objects.filter(
                event=event_id, participant__id=self.request.user.id
            ).exists()
            if is_subscribed:
                activities = list(
                    EventSubscription.objects.filter(
                        event=event_id,
                        participant__id=self.request.user.id,
                        is_subcription_canceled=False,
                    ).values_list("id", flat=True)
                )
                context["activities_subscribed"] = activities

        return context


@method_decorator(login_required, name="dispatch")
class EventSubscriptionView(View):
    model = EventSubscription
    template_name = "core/event_detail.html"

    def post(self, request, *args, **kwargs):
        participant = self.request.user.id
        request_data = self.request.POST
        event_id = request_data.get("event_id")

        activities_list = self.request.POST.getlist("selected_activities")
        try:
            activities_list = [int(activity_id) for activity_id in activities_list]

            if activities_list:
                for activity in activities_list:
                    subcription_instance, created = (
                        EventSubscription.objects.get_or_create(
                            event__id=event_id,
                            participant__id=participant,
                            activity__id=activity,
                        )
                    )
                    if not created:
                        subcription_instance.is_subcription_canceled = False
                        subcription_instance.save()

                Activity.objects.decrement_capacity(activities_list, value=1)
            else:
                return HttpResponse({"message": "Nao aceito isso!"})

        except Exception as exception:
            return HttpResponse({"message": f"Nao aceito isso! {exception}"})

        return HttpResponse({"message": "Nao aceito isso!"})

    def delete(self, request, *args, **kwargs):
        participant = self.request.user.id
        data = json.loads(request.body)
        event_id = data.get("event_id", None)

        try:
            if event_id:
                event_id = Event.objects.get(id=int(event_id)).id
            else:
                return JsonResponse(data={"error": "'event_id' is required"})
        except ValueError:
            return JsonResponse(data={"error": "Pass a integer 'event_id' value"})
        except Event.DoesNotExist:
            return JsonResponse(data={"error": "Event does not exist"})

        try:
            subcriptions = EventSubscription.objects.filter(
                event__id=event_id,
                participant__id=participant,
                is_subcription_canceled=False,
            )

            subcriptions.update(is_subcription_canceled=True)
            subcriptions_activities_ids = subcriptions.values_list(
                "activity", flat=True
            )
            print(subcriptions)
            Activity.objects.increment_capacity(
                list(subcriptions_activities_ids), value=1
            )

            return JsonResponse(data={"message": "Subscription cancelled succesfuly!"})
        except Exception as exception:
            return JsonResponse(
                data={
                    "exception": {"type": type(exception).__name__},
                    "Message": f"Exception raised during the subscription delete {str(exception)}",
                }
            )
