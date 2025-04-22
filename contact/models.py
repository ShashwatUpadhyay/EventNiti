from django.db import models
import uuid
# Create your models here.
class Contact(models.Model):
    uid = models.CharField(max_length=100, default=uuid.uuid4,unique=True)
    session_key = models.CharField(max_length=100,null=True,blank=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=60)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name + " " + self.subject