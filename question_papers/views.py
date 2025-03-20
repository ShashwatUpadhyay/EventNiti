from django.shortcuts import render , HttpResponse
from .  import models
from django.http import Http404
from ppuu import settings

# Create your views here.
def home(request):
    cource = models.Course.objects.all()
    return render(request, 'PreviousYearQuestionPaper.html', {'cources': cource}) 

def subject_page(request, c_name):
    try:
        course = models.Course.objects.get(name = c_name)
    except:
        if not settings.DEBUG:
            raise Http404("Page not found")
        
    subject = models.Subject.objects.filter(course = course)
    print(subject)
    return render(request, 'subject.html', {'subjects': subject,'c_name': c_name}) 

def exan_page(request,c_name,subject):
    exam = models.ExamName.objects.all()
    return render(request, 'exam_name.html', {'exams': exam, 'c_name': c_name, 'subject': subject}) 

def question_papers(request,c_name,exam, subject):
    try:
        course = models.Course.objects.get(name = c_name)
        exam = models.ExamName.objects.get(slug = exam)
        sub = models.Subject.objects.get(slug = subject)
    except:
        if not settings.DEBUG:
            raise Http404("Page not found")
        
    paper = models.PreviousYearQuestionPaper.objects.filter(course__name = c_name, exam_name__name = exam, subject__name = sub)   
    return render(request, 'question_papers.html', {'papers': paper}) 