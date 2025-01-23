from django.urls import path
from . import views
urlpatterns = [
    path('', views.events, name = 'events'),
    path('my-tickets/', views.myTicket , name='myticket'),
    path('<slug>/', views.event, name = 'event'),
    path('register/<slug>/', views.eventregister, name = 'eventregister'),
    path('ticket/<uid>', views.eventTicket, name='eventTicket'),
    path('attendence/<submissionid>/', views.takeSudentAttendence, name = 'takeSudentAttendence'),
]
