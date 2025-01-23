from django.contrib import admin

# Register your models here.
from .models import Event, EventSubmission,EventTicket

class EventSubmissionAdmin(admin.ModelAdmin):
    list_display = ('event', 'uu_id', 'full_name', 'email', 'course', 'section','attendence')
    search_fields = ('full_name', 'email','event__title', 'uu_id', 'course','attendence')
    list_filter = ('course', 'section', 'event')

class EventTicketAdmin(admin.ModelAdmin):
    list_display = ('event_submission','user')
    search_fields = ('event_submission','user')
    list_filter = ('event_submission','user')

admin.site.register(EventSubmission, EventSubmissionAdmin)

admin.site.register(Event)
admin.site.register(EventTicket)