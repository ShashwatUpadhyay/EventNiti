# Add this to one of your existing models.py files
from django.db import models
from django.contrib.auth.models import User
import json

class PushSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    endpoint = models.URLField(max_length=500)
    p256dh_key = models.CharField(max_length=100)
    auth_key = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def subscription_data(self):
        return {
            "endpoint": self.endpoint,
            "keys": {
                "p256dh": self.p256dh_key,
                "auth": self.auth_key
            }
        }
    
    def __str__(self):
        return f"Push subscription for {self.user.username if self.user else 'Anonymous'}"
    
    class Meta:
        verbose_name = "Push Subscription"
        verbose_name_plural = "Push Subscriptions"