from django.urls import path
from . import views
urlpatterns = [
    path('', views.event_memories_list, name = 'memories'),
    path('event/event_recape/<slug>/', views.event_recape, name = 'event_recacpe'),
    path('event/<event_slug>/upload/', views.UploadMemories, name = 'event_memory_upload'),
    path('event/<event_slug>/', views.event_memories_list, name = 'event_memories_list'),
]
