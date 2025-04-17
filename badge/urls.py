from django.urls import path
from . import views

urlpatterns = [
    path('' , views.badges , name='badges'),
    path('bulk_badge_destribution/<slug>/' , views.bulk_badge_destribution , name='bulk_badge_destribution'),
]