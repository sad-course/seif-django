import django_filters
import django_filters.widgets
from .models import Event

filtered_choices = Event.EventStatus.choices[1], Event.EventStatus.choices[2]


class EventFilter(django_filters.FilterSet):
    status = (
        django_filters.ChoiceFilter(
            choices=filtered_choices,
            label="Status",
        ),
    )
    campus = django_filters.ChoiceFilter(choices=Event.Campus.choices, label="Campus")

    class Meta:
        model = Event
        fields = ["status", "campus"]
