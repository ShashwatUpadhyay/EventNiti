
from django import template
from review.models import PollResponse,PollQuestion
from events.models import EventCordinator,EventSubmission
from django.shortcuts import get_object_or_404
register = template.Library()

@register.filter
def poll_voted(question, user):
    q_uid = question
    question = get_object_or_404(PollQuestion, uid = q_uid)
    return PollResponse.objects.filter(option__question=question,user=user).exists()

@register.filter
def is_host(event,user):
    return event.organized_by.username == user.username

@register.filter
def is_coordinator(event,user):
    return EventCordinator.objects.filter(user=user,event=event).exists()

@register.filter
def registered(event,user):
    return EventSubmission.objects.filter(event=event,user=user).exists()

@register.filter
def times(number):
    return range(int(number))

@register.filter
def review_count(event):
    review = event.reviews.all()
    return len(review)

@register.filter
def event_reviewed(event,user):
    return event.reviews.filter(user=user).exists()