from django.urls import path
from . import views
urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('<slug>/', views.blogpage, name='blogpage'),
]
