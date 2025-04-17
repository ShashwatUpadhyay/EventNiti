from django.urls import path
from . import views
urlpatterns = [
    path('', views.certificates, name='certificates'),
    path('<hash>', views.certificate, name='certificate'),
    path('bulk_certification/event/<slug>/', views.bulk_certification, name='bulk_certification'),
    path('distributed-cerificates/event/<slug>/', views.assign_cerificates, name='assign_cerificates'),
    path('edit_cert/<uid>/', views.edit_cert, name='edit_cert'),
    path('delete_cert/<uid>/', views.delete_cert, name='delete_cert'),
    path('create_cert/<user_>/<slug>/', views.create_cert, name='create_cert'),
    path('distributed-cerificates/event/<slug>/expot_csv/', views.cert_detail_csv, name='cert_detail_csv'),
]
