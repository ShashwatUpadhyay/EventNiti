from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
from account.models import UserExtra

# Create your views here.
def events(request):
    event = models.Event.objects.filter(event_open=True)
    return render(request, 'events.html',{'event':event})

def event(request, slug):
    try:
        event = models.Event.objects.get(slug= slug)
    except Exception as e:
        return redirect('home')
    return render(request, 'event.html',{'event':event})

def eventregister(request, slug):
    user_obj = None
    try:
        user_obj = UserExtra.objects.get(user=request.user)
    except Exception as e:
        print(e)
    try:
        event = models.Event.objects.get(slug= slug)
        if not event.registration_open:
            messages.error(request, "Registration is Closed!")
            return redirect('event', slug =slug)
    except Exception as e:
        return redirect('home')
    
    if request.method == "POST":
        uuid = request.POST.get('uuid')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        course = request.POST.get('course')
        section = request.POST.get('section')
        print(uuid,
            full_name,
            email,
            course,
            section,)
        submission = models.EventSubmission.objects.create(uu_id=uuid,full_name = full_name,email = email,course = course,section = section,event = event)
        messages.success(request,f"Submission Successful in {event.title} event")
        return redirect('events')
    return render(request, 'eventregister.html',{'event':event, 'user_obj':user_obj})
