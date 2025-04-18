from django.shortcuts import render,get_object_or_404, redirect
from . import models
from events.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from base.views import is_student
from django.http import HttpResponseRedirect

# Create your views here.
def memories(request):
    mem = models.Memories.objects.prefetch_related('memory_img').order_by('-event__start_date')
    return render(request, 'memories.html',{'mem':mem})

# def event_memories_list(request, event_slug):
#     event = get_object_or_404(Event, slug=event_slug)
#     memory = models.Memories.objects.get(event = event)
#     memories = event.memories_set.prefetch_related('memory_img', 'memory_vdo')
#     return render(request, 'event_memories_list.html', {'event': event, 'memories': memories,'memory':memory})

def event_memories_list(request):
    memories = models.MemoryImages.objects.all().order_by('-image_date')
    p = Paginator(memories,20)
    page = request.GET.get('page')
    memories = p.get_page(page)
    return render(request, 'all_memory_images.html', {'memories': memories})

@login_required(login_url='login')
def UploadMemories(request, event_slug):
    event = get_object_or_404(models.Event, slug=event_slug)
    memory,_ = models.Memories.objects.get_or_create(event=event)
    
    if request.method == 'POST':
        image_title = request.POST.get('title')
        image = request.FILES.get('image')

        if image_title and image:
            models.MemoryImages.objects.create(image_title=image_title, image=image,memory=memory,user=request.user)
            messages.success(request, "Memory image uploaded successfully!")
            return redirect('event_recacpe' , slug = event_slug)
        else:
            messages.error(request, "Please provide an image and title.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'uploadeventmemory.html')


def event_recape(request,slug):
    event = get_object_or_404(Event,slug=slug)
    images = models.MemoryImages.objects.filter(memory__event = event).order_by('-image_date')
    return render(request, 'events/recape.html',{'event':event,'images':images,'can_upload':True})

