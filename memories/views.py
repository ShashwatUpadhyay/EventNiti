from django.shortcuts import render,get_object_or_404
from . import models
from events.models import Event
# Create your views here.
def memories(request):
    mem = models.Memories.objects.prefetch_related('memory_img')
    return render(request, 'memories.html',{'mem':mem})

def event_memories_list(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    memories = event.memories_set.prefetch_related('memory_img', 'memory_vdo')
    return render(request, 'event_memories_list.html', {'event': event, 'memories': memories})
    # return render(request, 'event_memories_list.html', {'event': event, 'memories': memories})

