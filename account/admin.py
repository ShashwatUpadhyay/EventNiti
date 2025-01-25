from django.contrib import admin
from .models import *
# Register your models here.

class UserExtraAdmin(admin.ModelAdmin):
    list_display = ['full_name','uu_id','course','section','year','is_verified']
    search_fields = ['full_name','course','section','year','uu_id','is_verified']
    list_filter = ['year','section','course','is_verified']

admin.site.register(UserExtra, UserExtraAdmin)