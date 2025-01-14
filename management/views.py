from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'management/index.html') 

def organizers(request):
    return render(request, 'management/organizers.html')

def participants(request):
    return render(request, 'management/participants.html')
