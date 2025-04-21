from django.urls import path
from . import views
from account.views import profile
urlpatterns = [
    path('', views.home, name = 'home'),
    path('links/', views.socials, name = 'links'),
    path('profile/', profile, name = 'profile'),
    path('our-team/', views.ourTeam, name = 'ourTeam'),
    path('our-founding-team/', views.ourFoundingTeam, name = 'ourFoundingTeam'),
]
