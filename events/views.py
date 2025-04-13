from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from . import models
from django.contrib import messages
from django.contrib.auth.models import User
from account.models import UserExtra
from blog.models import Blog
from base.views import is_head, is_member, is_student, is_teacher
from certificate.views import generate_qr_code_base64
from django.contrib.auth.decorators import login_required
from ppuu import settings
from django.http import JsonResponse
import datetime
import pytz

india_timezone = pytz.timezone('Asia/Kolkata')

def is_cordinator(request,event):
    for event in event.cordinators.all():
        if request.user == event.user:
            return True
    return False

# Create your views here.
def events(request):
    event = models.Event.objects.filter(event_open=True,event_over = False).order_by('start_date').order_by('-registration_open')
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
    submission = get_object_or_404(models.EventSubmission , uid=submissionid)    
    if not is_cordinator(request,submission.event):
        messages.error(request , 'Access denied')
        return redirect('events')
    
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
        return redirect('events')
    
    event = models.Event.objects.filter(event_over=False, event_open=True).order_by('start_date')
    return render(request, 'eventsteacher.html',{'event':event})


@login_required(login_url='login')
def teacherEvent(request, slug):
    event = get_object_or_404(models.Event , slug=slug)
    if is_cordinator(request,event) or request.user.is_staff:
        return render(request, 'vieweventteacher.html',{'event':event})
    return redirect('events')

@login_required(login_url='login')
def registeredStudentList(request, slug):    
    students = models.EventSubmission.objects.filter(event__slug=slug).order_by('full_name')
    event = get_object_or_404(models.Event , slug=slug)
    if is_cordinator(request,event) or request.user.is_staff:
        return render(request , 'registeredstudent.html', {'students':students, 'event' : event}) 
    return redirect('events')

@login_required(login_url='login')
def registeredStudentListAjax(request, slug):
    if is_student(request.user):
        messages.error(request, "Access Denied!")
        return redirect('home')
    
    event = models.Event.objects.get(slug=slug)
    students = models.EventSubmission.objects.filter(event__slug=slug).order_by('full_name')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if it's an AJAX request
        student_data = []
        for student in students:
            student_data.append({
                "uu_id": student.uu_id,
                "full_name": student.full_name,
                "email": student.email,
                "course": student.course,
                "section": student.section,
                "year": student.year,
                "attendence": student.attendence,
                "attendence_taken_by": student.attendence_taken_by or "-",
                "allowed": "Yes" if student.allowed else "No"
            })
        return JsonResponse({"students": student_data})
    
    return render(request, 'registeredstudent.html', {'students': students, 'event': event})

def eventResult(request, slug):
    event =  None
    result =  None
    submisson =  None
    blog =  None
    try:
        event = models.Event.objects.get(slug=slug)
        submisson = models.EventSubmission.objects.filter(event = event)
        result = models.EventResult.objects.get(event = event)
        blogs = Blog.objects.filter(related_event = event)
    except Exception as e:
        messages.error(request,"No Result Announcement")
        return redirect('home')
    
    return render(request , 'resultofevent.html',{'event':event, 'result':result,'submisson':submisson,'blogs':blogs})