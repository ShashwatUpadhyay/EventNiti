from celery import shared_task
from . import settings
from django.core.mail import EmailMultiAlternatives,send_mail
from account.models import UserExtra
import logging
logger = logging.getLogger(__name__)

@shared_task
def event_announcement_task(emails, id):
    from events.models import Event    
    instance = Event.objects.get(id=id)
    try:
        subject = f'Join {instance.title}'
        text_content = f'Join {instance.title}. Click the link below to register:\n{settings.DOMAIN_NAME}events/{instance.slug}'
        html_content = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h1 style="color: #2d89ef;">We are thrilled to announce the {instance.title} event!</h1>
            <p>Click the link below to register for the event:</p>
            <a href="{settings.DOMAIN_NAME}events/{instance.slug}/" 
            style="display: inline-block; padding: 10px 20px; background-color: #2d89ef; color: #fff; text-decoration: none; border-radius: 5px;">
            Register Now
            </a>
            <p style="margin-top: 20px;">Thank you for your interest!</p>
        </div>
        """
        print('event@swtu.in')
        for email in emails:
            if UserExtra.objects.filter(user__email=email,is_verified=True).exists():
                send_mail(
                    subject=subject,
                    message=text_content,
                    from_email='event@swtu.in',
                    recipient_list=[email],
                    fail_silently=False,
                    html_message=html_content,
                )
            else:
                logger.info(f'User {email} is not verified. Skipping email sending for event {instance.title}.')

        # email = EmailMultiAlternatives(
        #     subject=subject,
        #     body=text_content,
        #     from_email='event@swtu.in',
        #     to=[],  # Keep "To" empty to avoid showing a main recipient
        #     bcc=emails[1:],  # Add all recipients in BCC
        # )
        # email.attach_alternative(html_content, "text/html")
        # email.send()
        logger.info(f'Event announcement email sent for event {instance.title} to {len(emails)} recipients.')
    except Exception as e:
        logger.error(f'Failed to send event announcement email for event {instance.title}. Error: {e}')
        print(e)

@shared_task     
def ticket_issued_email(instance_email, event_title ,ticket_uid):
    try:
        send_mail(
                'Ticket Issued',
                'You received a ticket from PPUU',
                'event@swtu.in',
                [instance_email],
                fail_silently=False,
                html_message=f"""<p>
                    <h1>Received {event_title} ticket</h1>
                    <a href='{settings.DOMAIN_NAME}events/ticket/{ticket_uid}'><button>OPEN</button></a>
                </p>"""
            )
        logger.info(f'Ticket issued email sent to {instance_email} for event {event_title}.')
    except Exception as e:
        logger.error(f'Failed to send ticket issued email to {instance_email} for event {event_title}. Error: {e}')
        print(e)


@shared_task        
def event_result_anouncement(emails, instance):
    try:
        subject =f'{instance.event.title} result is out!'
        text_content = f'{instance.event.title} result is out!'
        html_content = f"""<p>
                        <h1>We are thrilled to announce that {instance.event.title} event result is out!</h1>
                        <h4>Click the link below to see the result</h4>
                        <button><a href='{settings.DOMAIN_NAME}events/{instance.slug}/'>OPEN</a></button>
                    </p>"""
                    
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email='event@swtu.in',
            to=[],  # Keep "To" empty to avoid showing a main recipient
            bcc=emails[1:],  # Add all recipients in BCC
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(e)
        
@shared_task 
def certificate_issued_email(instance):
    print(instance['email'],instance['event'],instance['certificate_for'],instance['hash'])
    try:
        send_mail(
                'Congratulations!! You got Certificate from PPUU',
                'You received a Certificate from PPUU',
                'event@swtu.in',
                [instance['email']],
                fail_silently=False,
                html_message=f"""<p>
                    <h1>Received {instance['event']} {instance['certificate_for']} Certificate</h1>
                    <a href='{settings.DOMAIN_NAME}certificate/{instance['hash']}'><button>OPEN</button></a>
                </p>"""
            )
    except Exception as e:
        print(e)