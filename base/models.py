from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import User
from events.models import Event

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user} for {self.event} - {self.rating}/5"
 

# class PreviousYearCourse(models.Model):
#     choice = (('BCA', 'BCA'), ('MCA', 'MCA'),('BTECH', 'BTECH'),('DIPLOMA', 'DIPLOMA'))
#     year_choice = (('I', 'I'),('II', 'II'),('III', 'III'),('IV', 'IV'))
#     course = models.CharField(max_length=30,choices=choice)
#     year = models.CharField(max_length=10,choices=year_choice)
#     paper = models.FileField(upload_to='previous_year_question_paper/')
#     which_year = models.CharField(max_length=100, null=True, blank=True)
#     upload_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.course
    
class PreviousYearQuestionPaper(models.Model):
    choice = (('BCA', 'BCA'), ('MCA', 'MCA'),('BTECH', 'BTECH'),('DIPLOMA', 'DIPLOMA'))
    year_choice = (('I', 'I'),('II', 'II'),('III', 'III'),('IV', 'IV'))
    course = models.CharField(max_length=30,choices=choice)
    year = models.CharField(max_length=10,choices=year_choice)
    paper = models.FileField(upload_to='previous_year_question_paper/')
    which_year = models.CharField(max_length=100, null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.course
