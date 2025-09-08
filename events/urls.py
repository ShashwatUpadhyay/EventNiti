from django.urls import path
from . import views
urlpatterns = [
    path('', views.events, name = 'events'),
    path('create/', views.create_event, name='create_event'),
    path('my-tickets/', views.myTicket , name='myticket'),
    path('a/', views.teacherEventList, name = 'teacherEventList'),
    path('a/<slug>/', views.teacherEvent, name = 'teacherEvent'),
    path('a/<slug>/add_coordinators/', views.add_coordinators, name = 'add_coordinators'),
    path('a/remove_coordinator/<uid>/', views.remove_coordinator, name = 'remove_coordinator'),
    path('a/<slug>/edit/', views.edit_event, name = 'edit_event'),
    path('a/<slug>/registrations/', views.registeredStudentList, name = 'registeredStudentList'),
    path('a/<slug>/registration/', views.registeredStudentListAjax, name = 'registeredStudentListAjax'),
    path('<slug>/', views.event, name = 'event'),
    path('<slug>/result/', views.eventResult, name = 'eventResult'),
    path('register/<slug>/', views.eventregister, name = 'eventregister'),
    path('ticket/<uid>/', views.eventTicket, name='eventTicket'),
    path('attendence/<submissionid>/', views.takeSudentAttendence, name = 'takeSudentAttendence'),
    path('coordinator/my_coordinated_events/', views.my_coordinated_events, name = 'my_coordinated_events'),
    path('host/my_hosted_events/', views.my_hosted_events, name = 'my_hosted_events'),
    # path('live/polling_qna/', views.live_polling_qna, name = 'live_polling_qna'),
    path('a/<slug>/registrations/csv/', views.registeredStudentListExcel, name = 'registeredStudentListCSV'),
    
    # update description
    path('a/event_update/description/', views.update_description, name = 'update_description'),
    path('a/event_update/additional-description/', views.update_enrolled_description, name = 'update_enrolled_description'),
]

