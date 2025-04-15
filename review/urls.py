from django.urls import path
from . import views

urlpatterns = [
    path('poll/<slug>/', views.poll , name='poll'),
    path('qna/', views.qna , name='qna'),
]