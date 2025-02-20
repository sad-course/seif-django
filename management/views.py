from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import EventForm, EventPublishRequestForm, ActivityForm
from .models import Event, Tag, Activity, ActivityType


# Create your views here.
def index(request):
    return render(request, "management/index.html")


def organizers(request):
    return render(request, "management/organizers.html")


def participants(request):
    return render(request, "management/participants.html")


def analytics_home(request):
    return render(request, "management/analytics_home.html")


def analytics_event_detail(request):
    return render(request, "management/analytics_event_detail.html")


def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_event = Event.objects.create(
                title=data["title"],
                description=data["description"],
                banner=data["banner"],
                campus=data["campus"],
                status=data["initial_status"],
                init_date=data["init_date"],
                end_date=data["end_date"],
                created_by=request.user,
            )
            tag_names = data["tags"].split(",")
            tags = []

            for tag_name in tag_names:
                tag_name = tag_name.strip()
                tag = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)

            new_event.tags.set(tags)
            new_event.save()

            messages.success(request, "Evento criado!")
            return HttpResponseRedirect(reverse_lazy("create_event"))
    else:
        form = EventForm()

    return render(
        request,
        "management/create_event.html",
        {
            "form": form,
        },
    )


def create_activity(request, event_id):
    current_event = Event.objects.get(id=event_id)
    if request.method == "POST":
        form = ActivityForm()
        if form.is_valid():
            data = form.cleaned_data
            new_activity = Activity.objects.create(
                title=data["title"],
                description=data["description"],
                init_date=data["init_date"],
                end_date=data["end_date"],
                instructor=data["instructor"],
                estimated_duration=data["estimated_duration"],
                capacity=data["capacity"],
            )
            new_type = ActivityType.objects.create(name=data["activity_type"])
            new_activity.activity_type = new_type
            new_activity.event = current_event
            new_activity.save()
            return redirect("create_event", event_id=current_event.id)
    else:
        form = ActivityForm()

    return render(
        request, "management/create_event.html", {"form": form, "event": current_event}
    )


def request_create_event(request):
    if request.method == "POST":
        form = EventPublishRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # dados
            print(form.cleaned_data)
            return redirect(reverse_lazy("management"))
    else:
        form = EventPublishRequestForm()

    return render(request, "management/request_create_event.html", {"form": form})


def event_publish_requests(request):
    return render(request, "management/organizer_event_submit_requests.html")


def event_publish_request_detail(request):
    return render(request, "management/organizer_event_submit_detail.html")


def event_submit_dashboard(request):
    return render(request, "management/event_submit_dashboard.html")


def event_submit_detail(request):
    return render(request, "management/event_submit_detail.html")
