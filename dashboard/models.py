from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DashboardMetrics(models.Model):
    date = models.DateField(default=timezone.now)
    total_events = models.IntegerField(default=0)
    total_registrations = models.IntegerField(default=0)
    total_blogs = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    active_events = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ('date',)
        ordering = ['-date']

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=50)
    object_id = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    
    class Meta:
        ordering = ['-timestamp']