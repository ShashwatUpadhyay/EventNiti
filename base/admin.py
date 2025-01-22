from django.contrib import admin
from .models import Event, EventSubmission

admin.site.site_header = "Prerogative Pointers Administration"  
admin.site.site_title = "Prerogative Pointers Admin Portal"     
admin.site.index_title = "Welcome to Prerogative Pointers Admin Panel"  

# Register your models here.

class EventSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'uu_id', 'full_name', 'email', 'course', 'section','attendence')
    search_fields = ('full_name', 'email','event__title', 'uu_id', 'course','attendence')
    list_filter = ('course', 'section', 'event')

admin.site.register(EventSubmission, EventSubmissionAdmin)

admin.site.register(Event)
