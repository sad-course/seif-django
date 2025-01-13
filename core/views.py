from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')
  
def details(request):
    return render(request, 'core/event_detail.html')
  
def my_certificates(request):
    return render(request, 'core/my_certificates.html')

def my_events(request):
    return render(request, 'core/my_events.html')