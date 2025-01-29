from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.loginpage, name = 'login'),
    path('register/', views.registrationpage, name = 'register'),
    path('logout/', views.logoutpage, name = 'logout'),
    path('verify/<uid>/', views.accountVerify, name = 'verify'),
    path('forgot-password/', views.forgot_password, name = 'forgot_password'),
    path('changepassword/<uid>/', views.change_password, name = 'change_password'),
]
