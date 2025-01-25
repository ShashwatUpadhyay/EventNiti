from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class UserExtra(models.Model):
    uid = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    uu_id = models.CharField(max_length=30)
    roll_number = models.CharField(max_length=20, null=True, blank=True)
    year = models.CharField(max_length=5)
    is_verified = models.BooleanField(default=False)
    
    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name
    
    @property
    def username(self):
        return self.user.username
    
    @property
    def email(self):
        return self.user.email
    
    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)
    
    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        super(UserExtra, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural  = 'User Informations'
