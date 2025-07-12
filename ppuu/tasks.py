from celery import shared_task
from . import settings
from django.core.mail import EmailMultiAlternatives

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
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[],  # Keep "To" empty to avoid showing a main recipient
            bcc=emails[1:],  # Add all recipients in BCC
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(e)
    