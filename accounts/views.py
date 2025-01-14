from django.shortcuts import render

def my_certificates(request):
    return render(request, 'accounts/my_certificates.html')

def my_events(request):
    return render(request, 'accounts/my_events.html')