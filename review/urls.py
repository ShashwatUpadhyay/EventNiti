from django.urls import path
from . import views

urlpatterns = [
    path('poll/<slug>/', views.poll , name='poll'),
    path('qna/<slug>', views.qna , name='qna'),
    path('qna/qna_section/<slug>', views.qna_section , name='qna_section'),
    path('poll/poll_result/<slug>/', views.poll_result , name='poll_result'),
    path('poll/create/<slug>/', views.create_poll , name='create_poll'),
    path('poll/voters/<uid>/', views.voter_list_view , name='voters'),
    path('qna/delete_question/<uid>/', views.delete_question , name='delete_question'),
    path('qna/delete_answer/<uid>/', views.delete_answer , name='delete_answer'),
    path('event/reviews/<slug>/', views.event_reviews , name='event_reviews'),
]