from django.shortcuts import render,redirect
from . import models
from django.contrib import messages
from . import models
from account.models import UserExtra
from django.contrib.auth.models import User
from events.models import Event


# Create your views here.
def home(request):
    event = Event.objects.filter(event_open=True).order_by('start_date')[:3]
    return render(request , 'home.html',{'event':event})


def memories(request):
    return render(request, 'memories.html')

def contact(request):
    return render(request, 'contact.html')