from django.db import models
from account.models import User
from events.models import Event

class Course(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Section(models.Model):
    section = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.section
    
class Year(models.Model):
    year = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.year