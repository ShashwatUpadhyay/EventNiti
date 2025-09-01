# Push Notifications for Event Niti PWA
from pywebpush import webpush, WebPushException
import json
from django.conf import settings

class PushNotificationService:
    def __init__(self):
        self.vapid_private_key = getattr(settings, 'VAPID_PRIVATE_KEY', '')
        self.vapid_public_key = getattr(settings, 'VAPID_PUBLIC_KEY', '')
        self.vapid_claims = {
            "sub": "mailto:infernalknight96@gmail.com"
        }

    def send_notification(self, subscription_info, message_body, title="Event Niti"):
        """Send push notification to a single user"""
        try:
            response = webpush(
                subscription_info=subscription_info,
                data=json.dumps({
                    "title": title,
                    "body": message_body,
                    "icon": "/static/images/logo/android/android-launchericon-192-192.png",
                    "url": "/"
                }),
                vapid_private_key=self.vapid_private_key,
                vapid_claims=self.vapid_claims
            )
            return True
        except WebPushException as ex:
            print(f"Push notification failed: {ex}")
            return False

    def send_event_notification(self, event, message_type="new_event"):
        """Send notification about an event to all subscribers"""
        from .push_models import PushSubscription
        
        messages = {
            "new_event": f"New event: {event.title}",
            "event_reminder": f"Event starting soon: {event.title}",
            "registration_closing": f"Registration closing soon for: {event.title}",
            "certificate_ready": f"Your certificate is ready for: {event.title}"
        }
        
        message = messages.get(message_type, f"Update about: {event.title}")
        
        subscriptions = PushSubscription.objects.filter(is_active=True)
        success_count = 0
        
        for subscription in subscriptions:
            if self.send_notification(subscription.subscription_data, message):
                success_count += 1
        
        return success_count

# Usage in your views:
def send_event_notifications(event_id, message_type="new_event"):
    from events.models import Event
    
    try:
        event = Event.objects.get(id=event_id)
        notification_service = PushNotificationService()
        sent_count = notification_service.send_event_notification(event, message_type)
        print(f"Sent {sent_count} notifications for event: {event.title}")
    except Event.DoesNotExist:
        print("Event not found")