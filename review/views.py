from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from events.models import Event,EventSubmission
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from events.views import is_event_host, is_cordinator
from django.http import HttpResponseRedirect

# Create your views here.
@login_required(login_url='login')
def poll(request,slug):
    if not EventSubmission.objects.filter(user=request.user).exists():
        messages.error(request,'You are not registered in that event!')
        return redirect('events')
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


@login_required(login_url='login')
def poll_result(request,slug):
    event = get_object_or_404(Event,slug=slug)
    polls = models.PollQuestion.objects.filter(event=event).order_by('-created_at')
    
    
    polls_with_votes = []
    for poll in polls:
        options = poll.options.all()
        total_votes = sum(option.votes for option in options)
        polls_with_votes.append({
            "poll": poll,
            "options": options,
            "total_votes": total_votes,
        })


    context={
        'event':event,
        'poll':poll,
        "polls_with_votes": polls_with_votes,
        'is_host' : is_event_host(request,event),
        'is_cordinator' : is_cordinator(request,event),
    }
    return render(request,'review/poll_result.html',context)

@login_required(login_url='login')
def create_poll(request,slug):
    event = get_object_or_404(Event,slug=slug)
    if not is_event_host(request,event):
        messages.error(request,'Access denied!')
        return redirect('events')
    if request.method == "POST":
        question = request.POST.get('question')
        options = request.POST.getlist('options')
        
        poll = models.PollQuestion.objects.create(question=question,event=event)
        for option in options:
            models.PollOption.objects.create(question=poll,option=option)
        
        messages.success(request,"Poll uploaded")
        return redirect('teacherEvent', event.slug)
        
    return render(request,'review/create_poll.html',{'event':event})

@login_required(login_url='login')
def voter_list_view(request ,uid):
    option = get_object_or_404(models.PollOption,uid=uid)
    voters = models.PollResponse.objects.filter(option=option)
    return render(request, 'review/voters_list.html', {'voters': voters,'option':option})


def qna(request,slug):
    return render(request,'review/qna.html')

@login_required(login_url='login')
def qna_section(request,slug):
    event = get_object_or_404(Event,slug=slug)
    questions = models.QnaQuestion.objects.filter(event=event).order_by('-created_at')
    
    if request.method == 'POST':
        question = request.POST.get('question')
        
        if question:
            models.QnaQuestion.objects.create(user=request.user,question=question,event=event)
        
        for question in questions:
            answer = request.POST.get(question.uid)
            if answer:
                models.QnaAnswer.objects.create(answer=answer,question=question,user=request.user)

        return redirect('qna_section', slug)
    
    
    context = {
        'event':event,
        'questions':questions
    }
    return render(request,'review/qnas.html',context)

@login_required(login_url='login')
def delete_question(request,uid):
    question = get_object_or_404(models.QnaQuestion, uid=uid)
    question.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='login')
def delete_answer(request,uid):
    answer = get_object_or_404(models.QnaAnswer, uid=uid)
    answer.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))