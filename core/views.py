from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "core/index.html")


def details(request):
    return render(request, "core/event_detail.html")
