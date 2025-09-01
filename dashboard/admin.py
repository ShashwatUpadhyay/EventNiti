from django.contrib import admin
from .models import DashboardMetrics, ActivityLog

@admin.register(DashboardMetrics)
class DashboardMetricsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_events', 'total_registrations', 'total_blogs', 'total_users']
    list_filter = ['date']
    readonly_fields = ['date']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'description', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    readonly_fields = ['timestamp']
    search_fields = ['user__username', 'description']