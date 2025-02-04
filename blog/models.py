from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from account.models import User
from events.models import Event
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=400, null=True, blank=True, verbose_name='Slug (leave blank to auto-generate)')  
    content = CKEditor5Field(config_name='extends')
    image = models.ImageField(upload_to='blog_images/')
    related_event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, help_text="Select if the blog is related to the event else leave it", related_name='blogs')
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)   
    
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:   
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = '1. Blog'