import boto3
from botocore.exceptions import ClientError
from django.conf import settings

from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage

ses_client = boto3.client('ses', region_name='ap-south-1')

# try:
#     response = ses_client.verify_email_identity(
#         EmailAddress='example@example.com'
#     )
# except:
#     print('Email is not verified.')

# class SESEmailBackend(BaseEmailBackend):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client = boto3.client('ses', region_name='ap-south-1')  # change region

#     def send_messages(self, email_messages):
#         num_sent = 0
#         for message in email_messages:
#             try:
#                 response = self.client.send_email(
#                     Source=message.from_email,
#                     Destination={"ToAddresses": message.to},
#                     Message={
#                         "Subject": {"Data": message.subject},
#                         "Body": {
#                             "Text": {"Data": message.body},
#                             "Html": {"Data": message.body},
#                         },
#                     },
#                 )
#                 num_sent += 1
#             except Exception as e:
#                 if not self.fail_silently:
#                     raise
#         return num_sent


def send_ses_email(recipient, subject, body_text, body_html=None):
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [recipient],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body_html,
                    } if body_html else {},
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=settings.DEFAULT_FROM_EMAIL,
        )
    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
        return False
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")
        return True
    
