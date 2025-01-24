from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from ppuu import settings
from ppuu.mail_sender import event_anouncement,event_announcement
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
    notify = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)
        
class EventSubmission(models.Model):
    choice = (('Present','Present'),('Absent','Absent'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    uu_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    year = models.CharField(max_length=2)
    attendence = models.CharField(choices=choice, default='Absent', max_length=10)
    attendence_taken_by = models.CharField(max_length=60,null=True,blank=True)
    uid = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return str(self.full_name + " - " + self.event.title)
    
    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        super(EventSubmission, self).save(*args, **kwargs)
       
class EventTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    submission_uid = models.CharField(max_length=100, null=True, blank=True)
    uid = models.CharField(max_length=100, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        super(EventTicket, self).save(*args, **kwargs)
        
    def __str__(self):
        return str(self.user.get_full_name())
    
@receiver(post_save,sender = EventSubmission)
def generate_ticket(sender, instance, created,**kwargs):
    if created:
        ticket = EventTicket.objects.create(user = instance.user,submission_uid=instance.uid, event = instance.event)
        send_mail(
            'Ticket Issued',
            'You received a ticket from PPUU',
            settings.EMAIL_HOST_USER,
            [instance.user.email],
            fail_silently=False,
            html_message=f"""<p>
                <h1>Received {instance.event.title} ticket</h1>
                <a href='{settings.DOMAIN_NAME}events/ticket/{ticket.uid}'><button>OPEN</button></a>
            </p>"""
        )
        print('Ticket Created!')
        
        
@receiver(post_save,sender = Event)
def new_event_anouncement(sender, instance, created,**kwargs):
    if created:
        if instance.notify:
            emails = User.objects.values_list("email", flat=True)
            event_announcement(emails,instance)