from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('events/', views.events, name = 'events'),
    path('events/<slug>/', views.event, name = 'event'),
    path('events/register/<slug>/', views.eventregister, name = 'eventregister'),
    path('memories/', views.memories, name = 'memories'),
    path('contact/', views.contact, name = 'contact'),
]
