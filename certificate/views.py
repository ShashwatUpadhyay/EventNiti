from django.shortcuts import render,redirect, HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def certificate(request,hash):
    try:
        certi_obj = models.Certificate.objects.get(hash=hash)
    except Exception as e:
        return HttpResponse(f'No certificate with code: {hash}')
        
    return render(request ,'certificate.html', {'certi_obj':certi_obj})

@login_required(login_url='login')
def certificates(request):
    certi_obj = models.Certificate.objects.filter(user=request.user)
    return render(request ,'certificatecard.html', {'certi_obj':certi_obj})