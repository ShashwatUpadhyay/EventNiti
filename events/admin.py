from django.contrib import admin

# Register your models here.
from .models import Event, EventSubmission

class EventSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'uu_id', 'full_name', 'email', 'course', 'section','attendence')
    search_fields = ('full_name', 'email','event__title', 'uu_id', 'course','attendence')
    list_filter = ('course', 'section', 'event')

admin.site.register(EventSubmission, EventSubmissionAdmin)

admin.site.register(Event)