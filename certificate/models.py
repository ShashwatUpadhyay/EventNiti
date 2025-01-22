from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
import secrets 

# Create your models here.
def convert_date(date_obj):
    ist = pytz.timezone('Asia/Kolkata')
    ist_date = date_obj.astimezone(ist)
    return ist_date.strftime('%B %d, %Y %I:%M:%S %p')

class Certificate(models.Model):
    choices = (('Participation', 'Participation') ,('Winner', 'Winner'),('Runner Up', 'Runner Up'),('Second Runner-Up', 'Second Runner-Up'))
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    event = models.CharField(max_length=100)
    certificate_for = models.CharField(max_length=100, choices=choices, default='Participation')
    certificate_ss = models.ImageField(upload_to='certificates_ss/', null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        date = str(convert_date(self.issue_date))
        return f'{self.pk} - {self.user.username} - {self.event} - {date} - {self.hash}'
    def save(self, *args, **kwargs):
        # if not hash:
        
        super(Certificate, self).save(*args, **kwargs)

@receiver(post_save, sender = Certificate)
def save_certificate(sender,created, instance, **kwargs):
    if created:
        random_string = secrets.token_hex(16)
        instance.hash = hashlib.sha256(random_string.encode()).hexdigest()
        instance.save()
        print("Certificate Created")