from django.db import models
import uuid
from events.models import Event
from django.contrib.auth.models import User
# Create your models here.
class PollQuestion(models.Model):
    uid = models.CharField(max_length=100, default=uuid.uuid4)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='polls')
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        get_latest_by = 'crearted_at'
    
class PollOption(models.Model):
    uid = models.CharField(max_length=100, default=uuid.uuid4)
    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE,related_name='options')
    option = models.TextField()
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.option
    
class PollResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_responses')
    option = models.ForeignKey(PollOption , on_delete=models.CASCADE,related_name='voted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username + " " +  self.option.option
    
class QnaQuestion(models.Model):
    uid = models.CharField(max_length=100, default=uuid.uuid4)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
class QnaAnswer(models.Model):
    uid = models.CharField(max_length=100, default=uuid.uuid4)
    question = models.ForeignKey(QnaQuestion,on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer