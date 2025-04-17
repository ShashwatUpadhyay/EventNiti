
from django import template
from certificate.models import Certificate
from django.shortcuts import get_object_or_404
register = template.Library()

@register.filter
def get_cert_for(event,user):
    try:
        cert = Certificate.objects.filter(event=event,user=user)[0]
        return cert.certificate_for.title
    except:
        return ' - '

@register.filter
def get_cert_uid(event,user):
    try:
        uid = Certificate.objects.filter(event=event, user=user).values_list('hash', flat=True).first()
        return uid
    except:
        return None