from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "home"),
    path('details', views.details, name = "eventdetails"),
    path('my_certificates/', views.my_certificates, name = 'my_certificates'),
    path('my_events/', views.my_events, name = 'my_events'),
]
