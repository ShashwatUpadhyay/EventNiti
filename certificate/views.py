from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from . import models
from events.models import Event, EventSubmission
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import qrcode
import base64
from io import BytesIO
from ppuu import settings
from ppuu.settings import DOMAIN_NAME
from datetime import datetime
from django.template.loader import render_to_string
import base64
import os
from django.http import HttpResponseRedirect
import csv
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

def get_cert(event,user):
    try:
        cert = models.Certificate.objects.filter(event=event,user=user)[0]
        return cert.certificate_for.title
    except:
        return ' - '

def generate_certificate_link(student,certif_name, certi, dt):
    base_url = f"https://www.linkedin.com/profile/add?startTask={certif_name}"
    cert_name = f'{certif_name} Certificate'
    org_id = "103420170"  
    issue_year = dt.year
    issue_month = dt.month
    exp_year = ""
    exp_month = ""
    cert_url = f"{DOMAIN_NAME}certificates/{certi.hash}"
    cert_id = certi.hash

    linkedin_url = f"{base_url}&name={cert_name}&organizationId={org_id}" \
                   f"&issueYear={issue_year}&issueMonth={issue_month}" \
                   f"&expirationYear={exp_year}&expirationMonth={exp_month}" \
                   f"&certUrl={cert_url}&certId={cert_id}"

    return linkedin_url


def generate_qr_code_base64(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64

def certificate(request,hash):
    try:
        certi_obj = models.Certificate.objects.get(hash=hash)
    except Exception as e:
        return HttpResponse(f'No certificate with code: {hash}')
    dt = datetime.fromisoformat(str(certi_obj.issue_date))
    linkedin_url = generate_certificate_link(certi_obj.user, certi_obj.certificate_for.title, certi_obj,dt)  
    return render(request ,'certificate/templates/cert_v1.html', {'certi_obj':certi_obj,'linkedin_url':linkedin_url,'qr_code_base64': generate_qr_code_base64(f'{settings.DOMAIN_NAME}certificate/{certi_obj.hash}')})

@login_required(login_url='login')
def certificates(request):
    certi_obj = models.Certificate.objects.filter(user=request.user).order_by('-issue_date')
    return render(request ,'certificatecard.html', {'certi_obj':certi_obj})

from review.views import is_event_host,is_cordinator

@login_required(login_url='login')
def bulk_certification(request,slug):
    event = get_object_or_404(Event,slug=slug)
    if not is_event_host(request,event):
        return redirect('teacherEvent', event.slug)
    submission = EventSubmission.objects.filter(event=event)
    count = 0
    for sub in submission:
        if sub.attendence=='Present':
            models.Certificate.objects.get_or_create(event=event,user=sub.user,certificate_for=models.CertificateFor.objects.get(title='Participation'))
            count += 1
    event.cert_distributed = True
    event.save()
    messages.success(request,f'Certificates Sucessfully distributed for all present {count} participants in {event.title}')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url='login')
def assign_cerificates(request,slug):
    event = get_object_or_404(Event,slug=slug)
    students = EventSubmission.objects.filter(event=event)
    return render(request, 'certificate/assign_cerificates.html',{'students':students,'event':event})


@login_required(login_url='login')
def cert_detail_csv(request,slug):
    response = HttpResponse(content_type='text/csv')
    event = get_object_or_404(Event,slug=slug)
    students = EventSubmission.objects.filter(event=event)
    response['Content-Disposition'] = f'attachment; filename="{event.slug}_certification_list.csv"'

    writer = csv.writer(response)

    writer.writerow(['UUID', 'Full Name', 'Course', 'Section', 'Year', 'Attendence','Certified For'])
    
    for student in students:
        writer.writerow([
            student.uu_id,
            student.full_name,
            student.course,
            student.section,
            student.year,
            student.attendence,
            get_cert(event,student.user)
        ])

    return response

@login_required(login_url='login')
def edit_cert(request,uid):
    cert = get_object_or_404(models.Certificate, hash=uid)
    cert_for = models.CertificateFor.objects.all()
    
    if request.method == "POST":
        certificate_for=request.POST.get('certificate_for')
        cert.certificate_for=models.CertificateFor.objects.get(id=certificate_for)
        cert.save()
        messages.success(request, "Changes Applied Sucessfully!")
        return redirect('assign_cerificates', cert.event.slug)
    return render(request, 'certificate/edit_cert.html',{'cert':cert,'cert_for':cert_for})

@login_required(login_url='login')
def delete_cert(request,uid):
    cert = get_object_or_404(models.Certificate, hash=uid)
    cert.delete()
    messages.success(request, 'Certificate Deleted Sucessfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def create_cert(request,user_,slug):
    event = get_object_or_404(Event,slug=slug)
    user = get_object_or_404(User,username=user_)
    cert_for = models.CertificateFor.objects.all()
    if request.method == "POST":
        certificate_for=request.POST.get('certificate_for')
        models.Certificate.objects.create(event=event,user=user,certificate_for=models.CertificateFor.objects.get(id=certificate_for))
        messages.success(request, "Certificate Created!")
        return redirect('assign_cerificates', event.slug)
    return render(request, 'certificate/create_cert.html',{
        'user_':user,
        'event':event,
        'cert_for':cert_for,
    })
    
    
    