from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "management/index.html")


def analytics_home(request):
    return render(request, "management/analytics_home.html")
