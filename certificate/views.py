from django.shortcuts import render,redirect, HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import qrcode
import base64
from io import BytesIO
from ppuu import settings


def generate_qr_code_base64(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64

def certificate(request,hash):
    try:
        certi_obj = models.Certificate.objects.get(hash=hash)
    except Exception as e:
        return HttpResponse(f'No certificate with code: {hash}')
        
    return render(request ,'certificate.html', {'certi_obj':certi_obj,'qr_code_base64': generate_qr_code_base64(f'{settings.DOMAIN_NAME}certificate/{certi_obj.hash}')})

@login_required(login_url='login')
def certificates(request):
    certi_obj = models.Certificate.objects.filter(user=request.user)
    return render(request ,'certificatecard.html', {'certi_obj':certi_obj})