from django.db import models
from django.contrib.auth.models import User
import uuid
from events.models import Event
# Create your models here.
class Memories(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    memory_title = models.CharField(max_length=100, null=True,blank=True)
    memory_date  = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.event.title

class MemoryImages(models.Model):
    memory = models.ForeignKey(Memories,on_delete=models.CASCADE,related_name='memory_img')
    image_title = models.CharField(max_length=100, null=True,blank=True)
    image = models.ImageField(upload_to='memories_images/')
    image_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.image_date
    
    class Meta:
        get_latest_by = 'image_date'  


class MemoryVideo(models.Model):
    memory = models.ForeignKey(Memories,on_delete=models.CASCADE, related_name='memory_vdo')
    video_title = models.CharField(max_length=100, null=True,blank=True)
    video = models.FileField(upload_to='memories_videos/')
    video_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.video_date)