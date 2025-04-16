from django.contrib import admin
from .models import *
from ppuu.settings import COMPANY_NAME
admin.site.site_header = f"{COMPANY_NAME} Administration"  
admin.site.site_title = f"{COMPANY_NAME} Admin Portal"     
admin.site.index_title = f"Welcome to {COMPANY_NAME} Admin Panel"  

# Register your models here.
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Year)