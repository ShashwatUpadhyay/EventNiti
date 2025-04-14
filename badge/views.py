from django.shortcuts import render
from . import models
# Create your views here.

def badges(request):
    badge = models.Badge.objects.filter(user=request.user)
    return render(request,'badges.html',{'badges':badge})