from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('my_events/', views.my_certificates, name = 'my_events')
]
