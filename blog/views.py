from django.shortcuts import render
from . import models
# Create your views here.
def blogs(request):
    blogs = models.Blog.objects.filter(is_published=True).order_by('-upload_date')
    for blog in blogs:
        blog.first_line = blog.content.split('\n')[0]
    return render(request, 'blogpage.html', {'blog': blogs})

def blogpage(request,slug):
    blog = models.Blog.objects.get(slug=slug)
    return render(request, 'blog.html', {'blog': blog})