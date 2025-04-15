
from django import template
from review.models import PollResponse,PollQuestion
from django.shortcuts import get_object_or_404
register = template.Library()

@register.filter
def poll_voted(question, user):
    q_uid = question
    question = get_object_or_404(PollQuestion, uid = q_uid)
    return PollResponse.objects.filter(option__question=question,user=user).exists()