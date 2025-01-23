from django.urls import path
from . import views
urlpatterns = [
    path('', views.events, name = 'events'),
    path('<slug>/', views.event, name = 'event'),
    path('register/<slug>/', views.eventregister, name = 'eventregister'),
]
