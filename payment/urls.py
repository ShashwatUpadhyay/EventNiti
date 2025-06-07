from django.contrib import admin
from django.urls import path
from payment import views

urlpatterns = [
    path('<slug>/<token>/', views.event_payment, name='payment'),
    path('<slug>/<token>/paymenthandler/', views.paymenthandler, name='paymenthandler'),
]