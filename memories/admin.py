from django.contrib import admin
from .models import *
# Register your models here.

class AdminMemoryImages(admin.ModelAdmin):
    list_display = ['memory','image_title','image','image_date']
class AdminMemoryVideo(admin.ModelAdmin):
    list_display = ['memory','video_title','video','video_date']
    


admin.site.register(Memories)
admin.site.register(MemoryImages,AdminMemoryImages)
admin.site.register(MemoryVideo,AdminMemoryVideo)