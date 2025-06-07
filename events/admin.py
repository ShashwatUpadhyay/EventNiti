from django.contrib import admin

# Register your models here.
from .models import Event, EventSubmission,EventTicket,EventResult,EventCordinator, TemporaryEventSubmission
class EventSubmissionAdmin(admin.ModelAdmin):
    list_display = ('event', 'uu_id', 'full_name','course', 'section','year','allowed','attendence','attendence_taken_by')
    search_fields = ('full_name','event__title', 'uu_id','year', 'course','attendence')
    list_filter = ('course', 'section','year','event')

class EventTicketAdmin(admin.ModelAdmin):
    list_display = ('user__username','event__title','uid','created_at')
    search_fields = ('event__title','user__username','uid')
    list_filter = ('event__title','user__username')
    

class EventAdmin(admin.ModelAdmin):
    list_display = ('title','location', 'start_date','event_open','registration_open','notify')
    search_fields = ('title','organized_by__username', 'location','start_date')
    list_filter = ('event_open', 'registration_open', 'notify')

admin.site.register(EventSubmission, EventSubmissionAdmin)
admin.site.register(EventTicket,EventTicketAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(EventResult)
admin.site.register(EventCordinator)
admin.site.register(TemporaryEventSubmission)