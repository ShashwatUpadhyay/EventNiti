from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from ppuu import settings
from ppuu.mail_sender import event_anouncement, event_announcement,event_result_anouncement
# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=300, null=True,
                            blank=True, help_text=("Slug(leave it blank)"))
    poster = models.ImageField(
        upload_to='event_poster/', null=True, blank=True)
    description = models. TextField()
    organized_by = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True, blank=True)
    limit = models.IntegerField(null=True, blank=True, help_text=(
        'Limit (leave it blank if no registration limit)'))
    count = models.IntegerField(default=0)
    upload_time = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    event_open = models.BooleanField(default=True)
    registration_open = models.BooleanField(default=True)
    notify = models.BooleanField(default=True, help_text=(
        "Notify all users through email (at the time of creation)"))
    event_over = models.BooleanField(
        default=False, help_text=('Mark it True if the Event is Over'))
    text_status = models.CharField(
        max_length=100, null=True, blank=True, help_text=('let he backend handle it'))

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.registration_open == False:
            if not self.text_status:
                self.text_status = 'Registration Closed'
        if self.registration_open == True:
            if not self.text_status:
                self.text_status = 'Registration Open'
        super(Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-upload_time']
        verbose_name = '1. Event'

class EventSubmission(models.Model):
    choice = (('Present', 'Present'), ('Absent', 'Absent'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
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
    uid = models.CharField(max_length=100, null=True, blank=True)
    allowed = models.BooleanField(default=True)

    def __str__(self):
        return str(self.full_name + " - " + self.event.title)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = uuid.uuid4()
        super(EventSubmission, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = '2. Event Submission'


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
    

@receiver(post_save, sender=EventResult)
def resultAnounced(sender, instance, created, **kwargs):
    if instance.result_announced:
        emails = User.objects.values_list("email", flat=True)
        event_result_anouncement(emails, instance.event)

@receiver(post_save, sender=EventSubmission)
def generate_ticket(sender, instance, created, **kwargs):
    if created:
        ticket = EventTicket.objects.create(
            user=instance.user, submission_uid=instance.uid, event=instance.event)
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


@receiver(post_save, sender=Event)
def new_event_anouncement(sender, instance, created, **kwargs):
    if instance.event_open:
        if instance.notify:
            emails = User.objects.values_list("email", flat=True)
            event_announcement(emails, instance)


@receiver(post_delete, sender=EventSubmission)
def event_submission_deleted(sender, instance, **kwargs):
    instance.event.count -= 1
    instance.event.save()
