from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=300, null=True, blank=True)
    description = models. TextField()
    organized_by = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    event_open = models.BooleanField(default=True)
    registration_open = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)
        
class EventSubmission(models.Model):
    choice = (('Present','Present'),('Absent','Absent'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    uu_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    attendence = models.CharField(choices=choice, default='Absent', max_length=10)
    
    
    
# class Memories(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.CharField(max_length=300)
#     description = models.TextField()
#     date = models.DateField(null=True, blank=True)
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super(Memories, self).save(*args, **kwargs)
        
#     def __str__(self):
#         return str(self.title)
    
