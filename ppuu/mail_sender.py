from django.core.mail import send_mail
from . import settings
from django.core.mail import EmailMultiAlternatives

def verifyUser(email,uid):
    try:
        send_mail(
                    'Verify your account!',
                    'Verify your account',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    html_message=f"""<p>
                        <h1>Click the button below to verify your account 👇!</h1>
                        <button><a href='{settings.DOMAIN_NAME}user/verify/{uid}/'>OPEN</a></button>
                            
                    </p>"""
                )
    except Exception as e:  
        print(e)
    
def event_anouncement(emails,instance):
    try:
        for email in emails:
            send_mail(
                    f'Join {instance.title}',
                    f'Join {instance.title}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    html_message=f"""<p>
                        <h1>We are thrilled to announce the we organizing {instance.title} event</h1>
                        <h4>Click the link below to register in event</h4>
                        <button><a href='{settings.DOMAIN_NAME}events/{instance.slug}/'>OPEN</a></button>
                    </p>"""
                )
    except Exception as e:
        print(e)


def event_announcement(emails, instance):
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
            from_email=settings.EMAIL_HOST_USER,
            to=[],  # Keep "To" empty to avoid showing a main recipient
            bcc=emails[1:],  # Add all recipients in BCC
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(e)
    
def change_password_email(email, token):
    try:
        send_mail(
            'Reset Password',
            'Reset Password',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
            html_message=f"""<p>
                <h1>Click the button below to reset your password 👇!</h1>
                <button><a href='{settings.DOMAIN_NAME}user/changepassword/{token}/'>OPEN</a></button>
            </p>"""
        )
    except Exception as e:
        print(e)
    
def ticket_issued_email(instance,ticket):
    try:
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
    except Exception as e:
        print(e)
    
def certificate_issued_email(instance):
    try:
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
    except Exception as e:
        print(e)