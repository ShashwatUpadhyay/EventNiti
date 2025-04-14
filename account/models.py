from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.

class UserExtra(models.Model):
    uid = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_extra')
    phone = models.CharField(max_length=10, null= True, blank=True)
    course = models.CharField(max_length=10,null= True, blank=True)
    section = models.CharField(max_length=10,null= True, blank=True)
    uu_id = models.CharField(max_length=30,null= True, blank=True)
    roll_number = models.CharField(max_length=20, null=True, blank=True)
    year = models.CharField(max_length=5,null= True, blank=True)
    is_verified = models.BooleanField(default=False)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    forget_password_token_time = models.DateTimeField(null=True, blank=True)
    
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


@receiver(post_save , sender = User)
def createUserExtra(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser or instance.is_staff:
            user_extra, created = UserExtra.objects.get_or_create(user=instance)