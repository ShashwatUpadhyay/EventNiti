from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib import messages
from django.contrib.auth.models import User
from account.models import UserExtra
from certificate.views import generate_qr_code_base64, is_head, is_member, is_student, is_teacher
from django.contrib.auth.decorators import login_required

# Create your views here.
def events(request):
    event = models.Event.objects.filter(event_open=True)
    return render(request, 'events.html',{'event':event})

@login_required(login_url='login')
def event(request, slug):
    try:
        event = models.Event.objects.get(slug= slug)
    except Exception as e:
        return redirect('home')
    registered = False
    if models.EventSubmission.objects.filter(user=request.user, event=event).exists():
        messages.error(request, "You are Alredy Registered")
        registered = True
    return render(request, 'event.html',{'event':event,'registered':registered})

@login_required(login_url='login')
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
        if models.EventSubmission.objects.filter(user=request.user, event=event).exists():
            messages.error(request, "You are Alredy Registered")
            return redirect('event', slug =slug)
    except Exception as e:
        messages.error(request, f"Error: {e}   ")  
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
        submission = models.EventSubmission.objects.create(uu_id=uuid,full_name = full_name,email = email,user=request.user,course = course,section = section,event = event)
        messages.success(request,f"Submission Successful in {event.title} event")
        return redirect('events')
    return render(request, 'eventregister.html',{'event':event, 'user_obj':user_obj})


def eventTicket(request, uid):
    ticket = None
    submisson = None
    try:
        ticket = models.EventTicket.objects.get(uid=uid)
    except:
        return HttpResponse("invalid Ticket ID!")
    
    return render(request,'eventticket.html',{'ticket':ticket, 'qrCode':generate_qr_code_base64(f'http://127.0.0.1:8000/events/attendence/{ticket.submission_uid}')})
    
@login_required(login_url='login')
def myTicket(request):
    ticket = models.EventTicket.objects.filter(user = request.user)
    return render(request , 'tickets.html', {'ticket':ticket})
    
@login_required(login_url='login')
def takeSudentAttendence(request, submissionid):
    print()
    if is_student(request.user):
        messages.error(request,"Permission Denied!")
        return redirect('home')
    
    submission = None
    try:
        submission = models.EventSubmission.objects.get(uid=submissionid)
    except:
        return render(request, 'eventattendence.html', {'submission': False, 'msg': 'QR code is Expired'})
    
    if submission.attendence == 'Present':
        return render(request, 'eventattendence.html', {'submission': False, 'msg': 'Attendence Already Marked'})
    
    if submission.attendence == 'Absent':
        submission.attendence = 'Present'
        submission.save()
    return render(request, 'eventattendence.html', {'submission': True, 'msg': 'Attendence sucessfully Marked!! '})