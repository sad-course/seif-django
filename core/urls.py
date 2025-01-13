from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('my_certificates/', views.my_certificates, name = 'my_certificates'),
    path('my_events/', views.my_events, name = 'my_events'),
]
