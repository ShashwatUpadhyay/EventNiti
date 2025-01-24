from django.urls import path
from . import views
urlpatterns = [
    path('', views.memories, name = 'memories'),
    path('event/<event_slug>/', views.event_memories_list, name = 'event_memories_list'),
]
