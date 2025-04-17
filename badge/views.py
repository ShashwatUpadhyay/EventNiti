from django.shortcuts import render,get_object_or_404,redirect
from . import models
from events.models import Event, EventSubmission
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from review.views import is_event_host

# Create your views here.

def badges(request):
    badge = models.Badge.objects.filter(user=request.user)
    return render(request,'badges.html',{'badges':badge})

@login_required(login_url='login')
def bulk_badge_destribution(request,slug):
    event = get_object_or_404(Event,slug=slug)
    # if not is_event_host(request,event):
    #     return redirect('teacherEvent')
    submission = EventSubmission.objects.filter(event=event)
    count = 0
    for sub in submission:
        if sub.attendence=='Present':
            models.Badge.objects.get_or_create(event=event,user=sub.user,badge_name=f'{event.title} badge')
            count += 1
    event.badge_distributed = True
    event.save()
    messages.success(request,f'Badges Sucessfully distributed for all present {count} participants  in {event.title}')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))