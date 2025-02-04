from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import pytz
from django.db.models.signals import post_save
from django.dispatch import receiver
import hashlib
import secrets 
from events.models import Event
from django.core.mail import send_mail
from ppuu import settings
import uuid

# Create your models here.
def convert_date(date_obj):
    ist = pytz.timezone('Asia/Kolkata')
    ist_date = date_obj.astimezone(ist)
    return ist_date.strftime('%B %d, %Y %I:%M:%S %p')

class CertificateFor(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '2. Certificate Achievement'
        

class Certificate(models.Model):
    choices = (('Participation', 'Participation') ,('Winner', 'Winner'),('Runner Up', 'Runner Up'),('Second Runner-Up', 'Second Runner-Up'))
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    event = models.ForeignKey(Event,models.CASCADE)
    certificate_for = models.ForeignKey(CertificateFor, on_delete=models.CASCADE)
    certificate_ss = models.ImageField(upload_to='certificates_ss/', null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        date = str(convert_date(self.issue_date))
        return f'{self.user.get_full_name()} - {settings.DOMAIN_NAME}certificate/{self.hash}'
    def save(self, *args, **kwargs):
        super(Certificate, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-issue_date']
        verbose_name = '1. Certificate'
        
    
@receiver(post_save, sender = Certificate)
def save_certificate(sender,created, instance, **kwargs):
    if created:
        random_string = secrets.token_hex(16)
        instance.hash = uuid.uuid4()
        instance.save()
        send_mail(
            'Congratulations!! You got Certificate from PPUU',
            'You received a Certificate from PPUU',
            settings.EMAIL_HOST_USER,
            [instance.user.email],
            fail_silently=False,
            html_message=f"""<p>
                <h1>Received {instance.event.title} {instance.certificate_for} Certificate</h1>
                <a href='{settings.DOMAIN_NAME}certificate/{instance.hash}'><button>OPEN</button></a>
            </p>"""
        )
        print("Certificate Created")