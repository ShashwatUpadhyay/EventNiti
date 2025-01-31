from django.shortcuts import render,get_object_or_404, redirect
from . import models
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from base.views import is_student
# Create your views here.
def memories(request):
    mem = models.Memories.objects.prefetch_related('memory_img').order_by('-event__start_date')
    return render(request, 'memories.html',{'mem':mem})

def event_memories_list(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    memories = event.memories_set.prefetch_related('memory_img', 'memory_vdo')
    return render(request, 'event_memories_list.html', {'event': event, 'memories': memories})

@login_required(login_url='login')
def UploadMemories(request, event_slug):
    
    if is_student(request.user):
        messages.error(request, "You are not allowed to upload memories.")
        return redirect('event_memories_list', event_slug = event_slug)
    
    try:
        event = models.Event.objects.get(slug=event_slug)
        memory = models.Memories.objects.get(event=event)
    except Exception as e:
        messages.error(request, f"Something went wrong! {e}")
        return redirect('event_memories_list', event_slug = event_slug)
    
    if request.method == 'POST':
        image_title = request.POST.get('title')
        image = request.FILES.get('image')

        if image_title and image:
            models.MemoryImages.objects.create(image_title=image_title, image=image,memory=memory)
            messages.success(request, "Memory image uploaded successfully!")
            return redirect('event_memories_list', event_slug = event_slug)
        else:
            messages.error(request, "Please provide an image and title.")
    return render(request, 'uploadeventmemory.html')


