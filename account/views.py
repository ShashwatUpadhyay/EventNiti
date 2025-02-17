from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from ppuu.mail_sender import verifyUser, change_password_email
from django.core.cache import cache
import logging
import datetime
import pytz
import secrets

time_zone = pytz.timezone("Asia/Kolkata")
current_time = datetime.datetime.now(time_zone)

logger = logging.getLogger(__name__)
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
        user_obj=None
        try:
            user_obj = models.UserExtra.objects.get(user = user)
        except:
            user_obj = authenticate(username = username, password = password)
            if not user_obj:
                messages.error(request, "Invalid Credential")
                return redirect('login') 
            login(request,user_obj)
            logger.info(f'[{current_time}] {user_obj.get_full_name()} logged in')
            return redirect('/admin')
        
        if not user_obj.is_verified:
            if cache.get(username):
                data = cache.get(username)
                data['count'] += 1
            
                if data['count'] >= 3:
                    cache.set(username,data, 60*5)
                    messages.error(request,"You have exceeded the limit of verification mail!.. Please try again after 5 minutes.")
                    return redirect('login')
                cache.set(username,data, 60*1)
             
            if not cache.get(username):   
                data = {
                    'username':username,
                    'count': 1
                }
                cache.set(username,data, 60*1)
               
            verifyUser(user.email,user_obj.uid)
            messages.error(request,"Verification mail has been sent to the registered!.. Please verify your account.")
            return redirect('login')
        
        user_obj = authenticate(username = username, password = password)
        if not user_obj:
            messages.error(request, "Invalid Credential")
            return redirect('login')
        login(request,user_obj)
        logger.info(f'[{current_time}] {user_obj.get_full_name()} logged in')
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
        phone = request.POST.get('phone')
        course = request.POST.get('course')
        section = request.POST.get('section')
        year = request.POST.get('year')
        uuid = request.POST.get('uuid') 
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')
        
        if models.UserExtra.objects.filter(uu_id = uuid).exists():
            messages.error(request, 'UUID already Exists!')
            return redirect('register')
        if User.objects.filter(email = email).exists():
            messages.error(request, 'Email already Exists!')
            return redirect('register')
        if User.objects.filter(phone = phone).exists():
            messages.error(request, 'Mobile number already Exists!')
            return redirect('register')
        if len(str(phone))!=10:
            messages.error(request, 'Mobile number is Invalid!')
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
        models.UserExtra.objects.create(user = user_obj,phone=phone, uu_id = uuid, course = course, section = section,year=year,forget_password_token = secrets.token_hex(20),forget_password_token_time = current_time)
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
        
        
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not User.objects.filter(email = email).exists():
            messages.error(request, 'Email Not Found!')
            return redirect('forgot_password')
        user = User.objects.get(email = email)
        user_obj = models.UserExtra.objects.get(user = user)
        
        change_password_email(user.email,user_obj.forget_password_token)
        messages.success(request, 'Password Reset Link has been sent to the registered email!..')
        return redirect('forgot_password')
    return render(request, 'forgotpassword.html')  
       
        
def change_password(request,uid):
    user_obj = None
    try:
        user_obj = models.UserExtra.objects.get(forget_password_token = uid)
    except:
        return render(request,'invaliduser.html')
    
    if request.method == "POST":
        password = request.POST.get('password')
        re_password = request.POST.get('re-password')
        if password != re_password:
            messages.error(request, "Passwords doesn't not match")
            return redirect('change_password', uid = uid)
        user = user_obj.user
        user.set_password(password)
        user.save()
        user_obj.forget_password_token = secrets.token_hex(20)
        user_obj.forget_password_token_time = current_time
        user_obj.save()
        messages.success(request, 'Password Changed Successfully!')
        return redirect('login')
    return render(request, 'changepassword.html')  