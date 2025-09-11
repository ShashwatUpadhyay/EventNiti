from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from ppuu import settings
from ppuu.tasks import event_announcement_task,ticket_issued_email
from django.db.models import Avg
from events.choices import EVENT_STATUS
import logging
logger = logging.getLogger(__name__)
# Create your models here.


class Event(models.Model):
    uid = models.CharField(max_length=100, default=uuid.uuid4, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=300, null=True,
                            blank=True, help_text=("Slug(leave it blank)"))
    poster = models.ImageField(
        upload_to='event_poster/', null=True, blank=True)
    poster_url = models.URLField(max_length=500, null=True, blank=True)
    description = models. TextField()
    enrolled_description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField(
        default=0, help_text=('Price of the Event (leave it 0 if free)'))
    organized_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    location = models.CharField(max_length=100, null=True, blank=True)
    limit = models.IntegerField(null=True, blank=True,default=0, help_text=(
        'Limit (leave it blank if no registration limit)'))
    count = models.IntegerField(default=0)
    upload_time = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    last_date_of_registration = models.DateTimeField(null=True, blank=True)
    offers_certification = models.BooleanField(default=False)
    event_open = models.BooleanField(default=True)
    registration_open = models.BooleanField(default=True)
    notify = models.BooleanField(default=True, help_text=(
        "Notify all users through email (at the time of creation)"))
    event_over = models.BooleanField(
        default=False, help_text=('Mark it True if the Event is Over'))
    text_status = models.CharField(
        max_length=100, null=True, blank=True, help_text=('let he backend handle it'))
    cert_distributed = models.BooleanField(default=False)
    badge_distributed = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=EVENT_STATUS, default='pending')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
    @property
    def review_count(self):
        return len(self.reviews.all())
    
    @property
    def registration_count(self):
        return self.participant.count()
    
    @property
    def registered_percentage(self):
        if self.limit > 0:
            registrations = self.participant.count()
            percentage = (registrations / self.limit) * 100
            return percentage
        return 0
    
    @property
    def avg_rating(self):
        rate = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        star = int(rate) * '⭐'
        return star
    
    @property
    def get_image_url(self):
        if self.poster:
            return self.poster.url
        elif self.poster_url:
            return self.poster_url
        else:
            return settings.DEFAULT_EVENT_IMAGE_URL
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.registration_open == False:
            if not self.text_status:
                self.text_status = 'Registration Closed'
        if self.registration_open == True:
            if not self.text_status:
                self.text_status = 'Registration Open'
        super(Event,self).save(*args, **kwargs)

    class Meta:
        ordering = ['-upload_time']
        verbose_name = '1. Event'

class EventSubmission(models.Model):
    choice = (('Present', 'Present'), ('Absent', 'Absent'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participant')
    uu_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    year = models.CharField(max_length=5)
    attendence = models.CharField(
        choices=choice, default='Absent', max_length=10)
    attendence_taken_by = models.CharField(
        max_length=60, null=True, blank=True, verbose_name='Attendence Taken By/At ')
    uid = models.CharField(max_length=100, default=uuid.uuid4 ,null=True, blank=True)
    allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True,blank=True)

    def __str__(self):
        return str(self.full_name + " - " + self.event.title)
    
    class Meta:
        verbose_name = '2. Event Submission'

class TemporaryEventSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='temp_participant')
    uu_id = models.CharField(max_length=50)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    year = models.CharField(max_length=5)
    uid = models.CharField(max_length=100, default=uuid.uuid4 ,null=True, blank=True)

    def __str__(self):
        return str(self.full_name + " - " + self.event.title)

    class Meta:
        verbose_name = '6. Temporary Event Submission'
        
class EventTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    submission_uid = models.CharField(max_length=100, null=True, blank=True)
    uid = models.CharField(max_length=100, null=True,
                           blank=True, verbose_name='Ticket UID')
    created_at = models.DateTimeField(auto_now_add=True)
    restricted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        super(EventTicket, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.get_full_name())

    class Meta:
        verbose_name = '3. Event Ticket'

class EventResult(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='result')
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first')
    first_img = models.ImageField(upload_to='event_result_photo/', null=True, blank=True)
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second')
    second_img = models.ImageField(upload_to='event_result_photo/', null=True, blank=True)
    third = models.ForeignKey(User, on_delete=models.CASCADE, related_name='third')
    third_img = models.ImageField(upload_to='event_result_photo/', null=True, blank=True)
    result_announced = models.BooleanField(default=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.event.title) + " - " + "Result"
    
    class Meta:
        verbose_name = '4. Event Result'

class EventCordinator(models.Model):
    uid = models.CharField(max_length=100, default=uuid.uuid4, null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='cordinator')
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='cordinators')
    role = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.get_full_name()) + " - " + str(self.event.title)

    class Meta:
        verbose_name = '5. Event Cordinator'
        unique_together = ('user', 'event')
    

@receiver(post_save, sender=EventResult)
def resultAnounced(sender, instance, created, **kwargs):
    if instance.result_announced:
        emails = User.objects.values_list("email", flat=True)
        # event_result_anouncement(emails, instance.event)

@receiver(post_save, sender=EventSubmission)
def generate_ticket(sender, instance, created, **kwargs):
    if created:
        ticket = EventTicket.objects.create(
            user=instance.user, submission_uid=instance.uid, event=instance.event)
        ticket_issued_email.delay(instance.email,instance.event.title,ticket.uid)
        print('Ticket Created!')


@receiver(post_save, sender=Event)
def new_event_anouncement(sender, instance, created, **kwargs):
    if instance.event_open and instance.notify:
            pass


@receiver(post_delete, sender=EventSubmission)
def event_submission_deleted(sender, instance, **kwargs):
    pass

