from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from ppuu.mail_sender import verifyUser
# Create your views here.




def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.success(request, "Username Doesn't exists!")
            return redirect('login')
        user = User.objects.get(username = username)
        user_obj = models.UserExtra.objects.get(user = user)
        
        if not user_obj.is_verified:
            verifyUser(user.email,user_obj.uid)
            messages.error(request,"Verification mail has been sent to the registered!.. Please verify your account.")
            return redirect('login')
        
        user_obj = authenticate(username = username, password = password)
        if not user_obj:
            messages.error(request, "Invalid Credential")
            return redirect('login')
        login(request,user_obj)
        return redirect('home')
    
    return render(request , 'login.html')

def registrationpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        course = request.POST.get('course')
        section = request.POST.get('section')
        year = request.POST.get('year')
        uuid = request.POST.get('uuid') 
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')
        
        print(first_name,
                last_name,
                username,
                email,
                course,
                section,
                uuid,
                password,
                re_password,
                year)
        
        if models.UserExtra.objects.filter(uu_id = uuid).exists():
            messages.error(request, 'UUID already Exists!')
            return redirect('register')
        if User.objects.filter(email = email).exists():
            messages.error(request, 'Email already Exists!')
            return redirect('register')
        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username already Exists!')
            return redirect('register')
        if password != re_password:
            messages.error(request, "Passwords doesn't not match")
            return redirect('register')
       
        user_obj = User.objects.create(first_name = first_name, last_name = last_name, username = username,email = email)
        user_obj.set_password(password)
        user_obj.save()
        group = Group.objects.get(name='STUDENT')
        group.user_set.add(user_obj)
        models.UserExtra.objects.create(user = user_obj, uu_id = uuid, course = course, section = section,year=year)
        messages.success(request, 'Your Account has been Created!')
        return redirect('register')
        
        
    return render(request , 'register.html')

def accountVerify(request, uid):
    user_obj=None
    try:
        user_obj = models.UserExtra.objects.get(uid=uid)
    except:
        return render(request,'invaliduser.html')   
    
    if user_obj.is_verified:
        return render(request,'alreadyverified.html')   
    
    user_obj.is_verified = True
    user_obj.save()
    return render(request,'accountverified.html')   
        
        
    

def logoutpage(request):
    logout(request)
    return redirect('login')