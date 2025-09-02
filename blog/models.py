from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Count, Avg
from django.utils import timezone
from django.utils.html import strip_tags
from account.models import User
from events.models import Event
import uuid
import json

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#5a67d8', help_text='Hex color code')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

class BlogTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    ]
    
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    slug = models.CharField(max_length=400, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, blank=True, help_text='Brief description')
    content = CKEditor5Field(config_name='extends')
    featured_image = models.ImageField(upload_to='blog_images/', blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(BlogTag, blank=True)
    related_event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='blogs')
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Status and visibility
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(default=0, help_text='Estimated read time in minutes')
    share_count = models.PositiveIntegerField(default=0)
    
    # SEO and Social Media
    og_title = models.CharField(max_length=60, blank=True, help_text='Open Graph title')
    og_description = models.CharField(max_length=160, blank=True, help_text='Open Graph description')
    og_image = models.ImageField(upload_to='blog_og/', blank=True, help_text='Social media image')
    
    # Content Management
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    auto_save_data = models.JSONField(default=dict, blank=True, help_text='Auto-saved draft data')
    last_auto_save = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            self.excerpt = strip_tags(self.content)[:297] + '...'
        
        # Calculate read time (average 200 words per minute)
        if self.content:
            word_count = len(strip_tags(self.content).split())
            self.read_time = max(1, round(word_count / 200))
        
        # Auto-generate SEO fields
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
        if not self.og_title:
            self.og_title = self.title[:60]
        if not self.og_description and self.excerpt:
            self.og_description = self.excerpt[:160]
        
        # Handle soft delete
        if self.status == 'deleted' and not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published'
    
    @property
    def comment_count(self):
        return self.comments.filter(is_approved=True).count()
    
    @property
    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '1. Blog'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['slug']),
        ]

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'
    
    class Meta:
        ordering = ['-created_at']

class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('blog', 'user')

class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('blog', 'ip_address')

class BlogBookmark(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('blog', 'user')

class CommentReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    
    comment = models.ForeignKey(BlogComment, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('comment', 'user')

class BlogShare(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('copy_link', 'Copy Link'),
    ]
    
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

class NewsletterSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='newsletter_subscription')
    is_subscribed = models.BooleanField(default=True)
    frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], default='weekly')
    categories = models.ManyToManyField(BlogCategory, blank=True)
    last_sent = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.frequency}'

class BlogAnalytics(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    avg_read_time = models.FloatField(default=0.0, help_text='Average time spent reading in seconds')
    bounce_rate = models.FloatField(default=0.0, help_text='Percentage of users who left immediately')
    
    class Meta:
        unique_together = ('blog', 'date')
        ordering = ['-date']

class WritingChallenge(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('judging', 'Judging'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    theme = models.CharField(max_length=100, help_text='Challenge theme or topic')
    rules = models.TextField(help_text='Challenge rules and guidelines')
    
    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    judging_end_date = models.DateTimeField()
    
    # Constraints
    min_words = models.PositiveIntegerField(default=500)
    max_words = models.PositiveIntegerField(default=2000)
    allowed_categories = models.ManyToManyField(BlogCategory, blank=True)
    
    # Prizes and Recognition
    prizes = models.JSONField(default=list, help_text='List of prizes for winners')
    winner_badges = models.JSONField(default=list, help_text='Badges to award winners')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('challenge_detail', kwargs={'slug': self.slug})
    
    @property
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    @property
    def participant_count(self):
        return self.submissions.count()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class ChallengeSubmission(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('winner', 'Winner'),
        ('runner_up', 'Runner Up'),
        ('disqualified', 'Disqualified'),
    ]
    
    challenge = models.ForeignKey(WritingChallenge, on_delete=models.CASCADE, related_name='submissions')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='challenge_submissions')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_submissions')
    
    # Submission details
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    
    # Judging
    judge_score = models.FloatField(null=True, blank=True, help_text='Score out of 100')
    judge_feedback = models.TextField(blank=True)
    public_votes = models.PositiveIntegerField(default=0)
    
    # Awards
    position = models.PositiveIntegerField(null=True, blank=True, help_text='Final ranking position')
    badges_earned = models.JSONField(default=list)
    
    class Meta:
        unique_together = ('challenge', 'participant')
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f'{self.participant.username} - {self.challenge.title}'

class PushNotificationSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions')
    endpoint = models.URLField()
    p256dh_key = models.CharField(max_length=255)
    auth_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'endpoint')

class NotificationLog(models.Model):
    TYPE_CHOICES = [
        ('new_blog', 'New Blog Post'),
        ('comment', 'New Comment'),
        ('like', 'Blog Liked'),
        ('challenge', 'Writing Challenge'),
        ('newsletter', 'Newsletter'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    sent_via_push = models.BooleanField(default=False)
    sent_via_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']