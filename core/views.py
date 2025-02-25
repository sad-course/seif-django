import json
import logging
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import EventSubscription
from management.models import Activity, Event
from .filters import EventFilter

filtered_choices = Event.EventStatus.choices[1], Event.EventStatus.choices[2]
filtered_campus = Event.Campus.choices[1:]

logger = logging.getLogger(__name__)


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
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        event_filter = EventFilter(self.request.GET, queryset=queryset)
        queryset = event_filter.qs

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

        event = context["event"]
        if self.request.user.is_authenticated:
            is_subscribed = EventSubscription.objects.filter(
                event=event, participant__id=self.request.user.id
            ).exists()

            if is_subscribed:
                activities = list(
                    EventSubscription.objects.filter(
                        event=event,
                        participant_id=self.request.user.id,
                        is_subcription_canceled=False,
                    ).values_list("activity", flat=True)
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
            if not activities_list:
                messages.error(request, "É necessário passar alguma opção!")
                return redirect(
                    reverse_lazy("event_details", kwargs={"event_id": event_id})
                )

            for activity in activities_list:
                activity_instance = Activity.objects.get(id=activity)
                if activity_instance.has_capacity:
                    subcription_instance, created = (
                        EventSubscription.objects.get_or_create(
                            event_id=event_id,
                            participant_id=participant,
                            activity_id=activity,
                        )
                    )
                    if not created:
                        subcription_instance.is_subcription_canceled = False
                        subcription_instance.save()
                else:
                    messages.error(
                        request, f"Sem vagas para a atividade {activity_instance.title}"
                    )
                    return redirect(
                        reverse_lazy("event_details", kwargs={"event_id": event_id})
                    )
            Activity.objects.decrement_capacity(activities_list, value=1)

        except Exception as exception:
            logger.exception(
                "An exception was raised during the event subscription creation.\
                Exception:  %s, Message: %s",
                type(exception).__name__,
                str(exception),
            )
            messages.error(
                request, "An internal error has occurred. Please try again later."
            )
            return redirect(
                reverse_lazy("event_details", kwargs={"event_id": event_id})
            )

        return redirect(reverse_lazy("my_events"))


class EventSubscriptionDetailView(View):
    def get_event_id(self):
        event_id = self.kwargs.get("event_id", None)
        try:
            if event_id:
                event_id = Event.objects.get(id=int(event_id)).id
            else:
                return JsonResponse(data={"error": "'event_id' is required"})
        except ValueError:
            return JsonResponse(data={"error": "Pass a integer 'event_id' value"})
        except Event.DoesNotExist:
            return JsonResponse(data={"error": "Event does not exist"})

        return event_id

    def patch(self, request, *args, **kwargs):
        event_id = self.get_event_id()
        participant = self.request.user.id

        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            messages.error(request, "É necessário passar o event id")
            return JsonResponse(data={"error": "Provide the body data", "status": 400})

        selected_activities = data.get("selected_activities", [])
        try:

            selected_activities = [
                int(activity_id) for activity_id in selected_activities
            ]
            if not selected_activities:
                self.delete(request)

            activities_subscribed = EventSubscription.objects.filter(
                event__id=event_id,
                participant__id=participant,
                is_subcription_canceled=False,
            ).values_list("activity", flat=True)

            current_set = set(activities_subscribed)
            selected_set = set(selected_activities)

            subscriptions_to_add = selected_set - current_set
            subscriptions_to_remove = current_set - selected_set

            for activity in subscriptions_to_add:
                Activity.objects.get(id=activity)
                EventSubscription.objects.update_or_create(
                    event_id=event_id,
                    participant_id=participant,
                    activity_id=activity,
                    defaults={"is_subcription_canceled": False},
                )

            Activity.objects.decrement_capacity(subscriptions_to_add, value=1)

            EventSubscription.objects.filter(
                event_id=event_id,
                participant_id=participant,
                activity_id__in=subscriptions_to_remove,
            ).update(is_subcription_canceled=True)
            Activity.objects.increment_capacity(subscriptions_to_remove, value=1)

            return JsonResponse(data={"message": "Subscription updated succesfuly!"})

        except Exception as exception:
            logger.exception(
                "An exception was raised during the event subscription update.\
                Exception:  %s, Message: %s",
                type(exception).__name__,
                str(exception),
            )
            return JsonResponse(
                data={
                    "error": "An internal error has occurred. Please try again later.",
                },
                status=500,
            )

    def delete(self, request, *args, **kwargs):
        participant = self.request.user.id
        event_id = self.kwargs.get("event_id", None)

        try:
            subcriptions = EventSubscription.objects.filter(
                event__id=event_id,
                participant__id=participant,
                is_subcription_canceled=False,
            )

            subcriptions_activities_ids = list(
                subcriptions.values_list("activity", flat=True)
            )
            subcriptions.update(is_subcription_canceled=True)
            Activity.objects.increment_capacity(subcriptions_activities_ids, value=1)

            return JsonResponse(data={"message": "Subscription cancelled succesfuly!"})
        except Exception as exception:
            logger.exception(
                "An exception was raised during the event subscription deletion.\
                Exception:  %s, Message: %s",
                type(exception).__name__,
                str(exception),
            )
            return JsonResponse(
                data={
                    "error": "An internal error has occurred. Please try again later.",
                },
                status=500,
            )
