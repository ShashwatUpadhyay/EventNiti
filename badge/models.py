from django.db import models
from django.contrib.auth.models import User
from events.models import Event
import uuid
# Create your models here.
class Badge(models.Model):
    hash = models.CharField(max_length=100, default=uuid.uuid4)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    badge_name = models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.badge_name if self.badge_name else self.event.title
    
    def save(self, *args, **kwargs):
        if not self.badge_name:
            self.badge_name = self.event.title
        super(Badge, self).save(*args, **kwargs) 