from django.shortcuts import render

# Create your views here.

def profile(request):
    return render(request, 'accounts/profile.html')

def login(request):
    context = {}
    return render(request, 'accounts/login.html', context=context)

def signup(request):
    return render(request, 'accounts/signup.html')
