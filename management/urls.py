from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='management'), 
    path('organizers/', views.organizers ,  name = 'organizers'),
    path('participants/', views.participants , name = 'participants'),
]
