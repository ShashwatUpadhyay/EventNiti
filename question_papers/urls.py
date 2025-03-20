from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'paperHome'),
    path('<c_name>/', views.subject_page, name = 'subject_page'),
    path('<c_name>/<subject>/', views.exan_page, name = 'exam_page'),
    path('<c_name>/<subject>/<exam>/', views.question_papers, name = 'question_papers'),
]
