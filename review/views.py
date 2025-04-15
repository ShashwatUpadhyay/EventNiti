from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from events.models import Event
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def poll(request,slug):
    event = get_object_or_404(Event , slug=slug)
    polls = models.PollQuestion.objects.filter(event=event).order_by('created_at')
    
    if request.method == "POST":
        for poll in polls:
            res = request.POST.get(poll.uid)
            if res:
                option = get_object_or_404(models.PollOption, uid=res)
                option.votes += 1
                option.save()
                models.PollResponse.objects.create(user=request.user,option=option)            
                messages.success(request, "Your Response has been taken!")
        return redirect('event' , slug)

    return render(request,'review/live_poll.html',{'polls':polls})

def qna(request):
    return render(request,'review/qna.html')