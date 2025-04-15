from django.urls import path
from . import views

urlpatterns = [
    path('poll/<slug>/', views.poll , name='poll'),
    path('qna/', views.qna , name='qna'),
    path('poll/poll_result/<slug>/', views.poll_result , name='poll_result'),
    path('poll/create/<slug>/', views.create_poll , name='create_poll'),
    path('poll/voters/<uid>/', views.voter_list_view , name='voters'),
]