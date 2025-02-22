from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
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
        context["campus_choices"] = Event.Campus.choices
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
