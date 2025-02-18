import django_filters
import django_filters.widgets
from .models import Event


class EventFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=Event.EventStatus.choices,
        label="Status",
    )

    class Meta:
        model = Event
        fields = ["status"]
