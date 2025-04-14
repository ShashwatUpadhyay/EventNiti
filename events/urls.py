from django.urls import path
from . import views
urlpatterns = [
    path('', views.events, name = 'events'),
    path('my-tickets/', views.myTicket , name='myticket'),
    path('auth-view/', views.teacherEventList, name = 'teacherEventList'),
    path('auth-view/<slug>/', views.teacherEvent, name = 'teacherEvent'),
    path('auth-view/<slug>/edit/', views.edit_event, name = 'edit_event'),
    path('auth-view/<slug>/registrations/', views.registeredStudentList, name = 'registeredStudentList'),
    path('auth-view/<slug>/registration/', views.registeredStudentListAjax, name = 'registeredStudentListAjax'),
    path('<slug>/', views.event, name = 'event'),
    path('<slug>/result/', views.eventResult, name = 'eventResult'),
    path('register/<slug>/', views.eventregister, name = 'eventregister'),
    path('ticket/<uid>/', views.eventTicket, name='eventTicket'),
    path('attendence/<submissionid>/', views.takeSudentAttendence, name = 'takeSudentAttendence'),
    path('coordinator/my_coordinated_events/', views.my_coordinated_events, name = 'my_coordinated_events'),
    path('host/my_hosted_events/', views.my_hosted_events, name = 'my_hosted_events'),
]
