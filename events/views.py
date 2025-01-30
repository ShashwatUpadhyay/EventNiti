from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib import messages
from django.contrib.auth.models import User
from account.models import UserExtra
from base.views import is_head, is_member, is_student, is_teacher
from certificate.views import generate_qr_code_base64
from django.contrib.auth.decorators import login_required
from ppuu import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
import datetime
import pytz

india_timezone = pytz.timezone('Asia/Kolkata')

# Create your views here.
def events(request):
    event = models.Event.objects.filter(event_open=True).order_by('start_date')
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
    event=None
    try:
        user_obj = UserExtra.objects.get(user=request.user)
    except Exception as e:
        print(e)
    try:
        event = models.Event.objects.get(slug= slug)
        if  event.event_over:
            messages.error(request, "Event is Over!")
            return redirect('event',slug =slug)
        if not event.registration_open:
            messages.error(request, "Registration is Closed!")
            return redirect('event', slug =slug)
        if models.EventSubmission.objects.filter(user=request.user, event=event).exists():
            messages.error(request, "Rejected!")
            return redirect('event', slug =slug)
    except Exception as e:
        messages.error(request, f"Error: {e}   ")  
        return redirect('home')
    
    if event.limit and event.count >= event.limit:
        event.registration_open = False
        event.text_status = 'Registration Full'
        event.save()    
        messages.error(request, "Registration is Full!")
        return redirect('event', slug =slug)
    
    if request.method == "POST":
        uuid = request.POST.get('uuid')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        course = request.POST.get('course')
        section = request.POST.get('section')
        year = request.POST.get('year')
        submission = models.EventSubmission.objects.create(uu_id=uuid,full_name = full_name,year=year,email = email,user=request.user,course = course,section = section,event = event)
        event.count = event.count + 1
        event.save()
        
        # #django channel
        # students = list(models.EventSubmission.objects.filter(event__slug=slug).values())
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     f"event_{slug}",
        #     {"type": "send_update", "students": students}
        # )
        
        messages.success(request,f"Submission Successful in {event.title} event")
        return redirect('events')

    return render(request, 'eventregister.html',{'event':event, 'user_obj':user_obj})

def update_registered_students(event_slug):
    channel_layer = get_channel_layer()
    students = models.EventSubmission.objects.filter(event__slug=event_slug).order_by('full_name')
    student_data = list(students.values("uu_id", "full_name", "email", "course", "section", "year", "attendence", "attendence_taken_by", "allowed"))

    async_to_sync(channel_layer.group_send)(
        f"event_{event_slug}",
        {"type": "send_student_update", "data": student_data}
    )


def eventTicket(request, uid):
    ticket = None
    submisson = None
    try:
        ticket = models.EventTicket.objects.get(uid=uid)
    except:
        return HttpResponse("invalid Ticket ID!")
    
    return render(request,'eventticket.html',{'ticket':ticket, 'qrCode':generate_qr_code_base64(f'{settings.DOMAIN_NAME}events/attendence/{ticket.submission_uid}/')})
    
@login_required(login_url='login')
def myTicket(request):
    ticket = models.EventTicket.objects.filter(user = request.user).order_by('-created_at')
    return render(request , 'tickets.html', {'ticket':ticket})
    
@login_required(login_url='login')
def takeSudentAttendence(request, submissionid):
    if is_student(request.user):
        messages.error(request,"Access Denied!")
        return redirect('home')
    
    submission = None
    try:
        submission = models.EventSubmission.objects.get(uid=submissionid)
    except:
        return render(request, 'eventattendence.html', {'submission': False, 'msg': 'Invalid QR Code', 'student': None})
    
    if models.EventTicket.objects.get(submission_uid=submissionid).restricted:
        return render(request, 'eventattendence.html', {'submission': False, 'msg': 'Student is Restricted!', 'student': submission.full_name})

    if not submission.allowed:
        return render(request, 'eventattendence.html', {'submission': False, 'msg': 'Candidate is not allowed!', 'student': submission.full_name})
    
    if submission.attendence == 'Present':
        return render(request, 'eventattendence.html', {'submission': False, 'msg': 'Attendence Already Marked', 'student': submission.full_name})
    
    if submission.attendence == 'Absent':
        current_time_india = datetime.datetime.now(india_timezone)
        submission.attendence = 'Present'
        submission.attendence_taken_by = f'{request.user.get_full_name()} - {current_time_india.strftime('%Y-%m-%d %I:%M:%S %p')}'
        submission.save()
        
    return render(request, 'eventattendence.html', {'submission': True, 'msg': 'Attendence sucessfully Marked!! ', 'student': submission.full_name})  


@login_required(login_url='login')
def teacherEventList(request):
    if is_student(request.user):
        messages.error(request,"Access Denied!")
        return redirect('home')
    
    event = models.Event.objects.all().order_by('start_date')
    return render(request, 'eventsteacher.html',{'event':event})


@login_required(login_url='login')
def teacherEvent(request, slug):
    if is_student(request.user):
        messages.error(request,"Access Denied!")
        return redirect('home')
    
    event = models.Event.objects.get(slug=slug)
    return render(request, 'vieweventteacher.html',{'event':event})

@login_required(login_url='login')
def registeredStudentList(request, slug):
    if is_student(request.user):
        messages.error(request,"Access Denied!")
        return redirect('home')
    
    students = models.EventSubmission.objects.filter(event__slug=slug).order_by('full_name')
    event = None
    try:
        event = models.Event.objects.get(slug=slug)
    except:
        return redirect('teacherEventList')
    
    return render(request , 'registeredstudent.html', {'students':students, 'event' : event}) 