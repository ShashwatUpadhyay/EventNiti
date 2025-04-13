from django.urls import path
from . import views
urlpatterns = [
    path('', views.certificates, name='certificates'),
    path('<hash>', views.certificate, name='certificate'),
    path('pdf/<hash>', views.certificate_generate_pdf, name='certificate_generate_pdf')
]
