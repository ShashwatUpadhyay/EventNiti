from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('previous-year-question-paper/', views.previous_paper, name = 'previous_paper'),
    path('contact/', views.contact, name = 'contact'),
    path('links/', views.socials, name = 'links'),
    path('our-team/', views.ourTeam, name = 'ourTeam'),
    path('our-founding-team/', views.ourFoundingTeam, name = 'ourFoundingTeam'),
]
