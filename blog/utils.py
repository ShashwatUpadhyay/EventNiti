from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import NewsletterSubscription, BlogAnalytics, PushNotificationSubscription, NotificationLog
import json
import requests
from datetime import datetime, timedelta

def auto_save_blog(blog_id, content_data, user):
    """Auto-save blog draft data"""
    from .models import Blog
    try:
        blog = Blog.objects.get(id=blog_id, user=user)
        blog.auto_save_data = content_data
        blog.last_auto_save = timezone.now()
        blog.save(update_fields=['auto_save_data', 'last_auto_save'])
        return True
    except Blog.DoesNotExist:
        return False

def track_blog_analytics(blog, request, action='view'):
    """Track detailed blog analytics"""
    today = timezone.now().date()
    analytics, created = BlogAnalytics.objects.get_or_create(
        blog=blog, date=today,
        defaults={'views': 0, 'unique_views': 0, 'likes': 0, 'comments': 0, 'shares': 0}
    )
    
    if action == 'view':
        analytics.views += 1
        # Track unique views by IP (simplified)
        if not blog.views.filter(ip_address=get_client_ip(request)).exists():
            analytics.unique_views += 1
    elif action == 'like':
        analytics.likes += 1
    elif action == 'comment':
        analytics.comments += 1
    elif action == 'share':
        analytics.shares += 1
    
    analytics.save()

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def send_newsletter(frequency='weekly'):
    """Send newsletter to subscribers"""
    from .models import Blog
    
    # Get date range based on frequency
    now = timezone.now()
    if frequency == 'daily':
        start_date = now - timedelta(days=1)
    elif frequency == 'weekly':
        start_date = now - timedelta(weeks=1)
    else:  # monthly
        start_date = now - timedelta(days=30)
    
    # Get recent published blogs
    recent_blogs = Blog.objects.filter(
        status='published',
        published_at__gte=start_date
    ).order_by('-published_at')[:10]
    
    if not recent_blogs:
        return
    
    # Get subscribers for this frequency
    subscribers = NewsletterSubscription.objects.filter(
        is_subscribed=True,
        frequency=frequency
    ).select_related('user')
    
    for subscription in subscribers:
        # Filter blogs by user's preferred categories
        user_blogs = recent_blogs
        if subscription.categories.exists():
            user_blogs = recent_blogs.filter(category__in=subscription.categories.all())
        
        if user_blogs:
            # Send email
            context = {
                'user': subscription.user,
                'blogs': user_blogs,
                'frequency': frequency,
                'unsubscribe_url': f"{settings.DOMAIN_NAME}blog/newsletter/unsubscribe/{subscription.user.id}/"
            }
            
            html_message = render_to_string('blog/newsletter_email.html', context)
            send_mail(
                subject=f'Event Niti Blog Digest - {frequency.title()}',
                message='',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
                html_message=html_message,
                fail_silently=True
            )
            
            # Update last sent
            subscription.last_sent = now
            subscription.save()

def send_push_notification(user, title, message, blog=None):
    """Send push notification to user"""
    subscriptions = PushNotificationSubscription.objects.filter(user=user, is_active=True)
    
    for subscription in subscriptions:
        payload = {
            'title': title,
            'body': message,
            'icon': '/static/images/logo/icon-192x192.png',
            'badge': '/static/images/logo/icon-72x72.png',
            'data': {
                'url': blog.get_absolute_url() if blog else '/blog/',
                'blog_id': blog.id if blog else None
            }
        }
        
        # Send notification (simplified - in production use proper web push library)
        try:
            # This would use a proper web push library like pywebpush
            # For now, just log the notification
            NotificationLog.objects.create(
                user=user,
                type='new_blog' if blog else 'general',
                title=title,
                message=message,
                blog=blog,
                sent_via_push=True
            )
        except Exception:
            pass

def generate_social_meta_tags(blog):
    """Generate social media meta tags for blog"""
    return {
        'og:title': blog.og_title or blog.title,
        'og:description': blog.og_description or blog.excerpt,
        'og:image': blog.og_image.url if blog.og_image else (blog.featured_image.url if blog.featured_image else ''),
        'og:url': f"{settings.DOMAIN_NAME.rstrip('/')}{blog.get_absolute_url()}",
        'og:type': 'article',
        'twitter:card': 'summary_large_image',
        'twitter:title': blog.og_title or blog.title,
        'twitter:description': blog.og_description or blog.excerpt,
        'twitter:image': blog.og_image.url if blog.og_image else (blog.featured_image.url if blog.featured_image else ''),
    }

def soft_delete_blog(blog):
    """Soft delete a blog post"""
    blog.status = 'deleted'
    blog.is_deleted = True
    blog.deleted_at = timezone.now()
    blog.save()

def restore_blog(blog):
    """Restore a soft-deleted blog post"""
    blog.status = 'draft'
    blog.is_deleted = False
    blog.deleted_at = None
    blog.save()