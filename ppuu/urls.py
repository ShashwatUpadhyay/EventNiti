"""
URL configuration for ppuu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),    
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('', include('base.urls')),
    path('user/', include('account.urls')),
    path('certificate/', include('certificate.urls')),
    path('badge/', include('badge.urls')),
    path('events/', include('events.urls')),
    path('memories/', include('memories.urls')),
    path('blog/', include('blog.urls')),
    path('review/', include('review.urls')),
    path('contact/', include('contact.urls')),
    path('payment/', include('payment.urls')),
    path('previous-year-question-paper/', include('question_papers.urls')),
]+ debug_toolbar_urls()
handler404 = 'base.views.custom_404'
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
