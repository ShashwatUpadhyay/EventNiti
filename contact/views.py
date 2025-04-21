from django.shortcuts import render,redirect
from . import models
import uuid
from django.contrib import messages

# Create your views here.
def contact(request):
    if request.method == "POST":
        name =  request.POST.get('name')
        email =  request.POST.get('email')
        subject =  request.POST.get('subject')
        main =  request.POST.get('message')
        
        if not request.session.get('ukey'):
            request.session['ukey'] = str(uuid.uuid4())
        models.Contact.objects.create(full_name = name,email = email,subject = subject,message = main,session_key=request.session['ukey'])
        messages.success(request, 'Your message has been sent! we will respond within 24 hour.')
        return redirect('contact')
    return render(request, 'contact.html')