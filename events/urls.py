from django.urls import path
from . import views
urlpatterns = [
    path('', views.events, name = 'events'),
    path('my-tickets/', views.myTicket , name='myticket'),
    path('auth-view/', views.teacherEventList, name = 'teacherEventList'),
    path('auth-view/<slug>/', views.teacherEvent, name = 'teacherEvent'),
    path('auth-view/<slug>/registrations/', views.registeredStudentList, name = 'registeredStudentList'),
    path('<slug>/', views.event, name = 'event'),
    path('register/<slug>/', views.eventregister, name = 'eventregister'),
    path('ticket/<uid>', views.eventTicket, name='eventTicket'),
    path('attendence/<submissionid>/', views.takeSudentAttendence, name = 'takeSudentAttendence'),
    
    # for teahcer view
]
