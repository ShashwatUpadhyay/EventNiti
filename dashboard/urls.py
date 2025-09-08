from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('events/', views.events_management, name='events'),
    path('events/approvals/', views.event_approvals, name='event_status'),
    path('events/approval/action/', views.approve_event, name='approve_event'),
    path('blogs/', views.blogs_management, name='blogs'),
    path('registrations/', views.registrations_view, name='registrations'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('users/', views.users_management, name='users'),
    path('api/quick-stats/', views.quick_stats_api, name='quick_stats_api'),
]