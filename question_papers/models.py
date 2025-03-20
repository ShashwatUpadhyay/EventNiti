from django.db import models
from django.utils.text import slugify

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = '5. Department'

class Year(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = '4. Year'

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return self.name + f' ({(self.department.name)})'
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Subject, self).save(*args, **kwargs)
    
    class Meta: 
        verbose_name = '2. Subject'

class ExamName(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        if not self.slug:
            self.slug = slugify(self.name)
        return super(ExamName, self).save(*args, **kwargs)
    
    class Meta: 
        verbose_name = '3. Exam Name'

class PreviousYearQuestionPaper(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_name = models.ForeignKey(ExamName, on_delete=models.CASCADE)
    paper = models.FileField(upload_to='previous_year_question_paper/')
    which_year = models.CharField(max_length=100, null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.course.name + ' - ' + self.exam_name.name
    
    class Meta: 
        verbose_name = '1. Previous Year Question Paper'
