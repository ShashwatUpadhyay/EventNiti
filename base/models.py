from django.db import models

    
# class Memories(models.Model):
#     title = models.CharField(max_length=200)
#     slug = models.CharField(max_length=300)
#     description = models.TextField()
#     date = models.DateField(null=True, blank=True)
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super(Memories, self).save(*args, **kwargs)
        
#     def __str__(self):
#         return str(self.title)
    
