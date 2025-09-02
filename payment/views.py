from django.shortcuts import render, get_object_or_404, redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from events.models import Event, TemporaryEventSubmission, EventSubmission
from django.contrib import messages 
from .models import Payment
import logging
logger = logging.getLogger(__name__)

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def event_payment(request,slug, token):
    event  = get_object_or_404(Event, slug=slug)
    tempSub = get_object_or_404(TemporaryEventSubmission, uid=token)
    currency = 'INR'
    amount = event.price*100 

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    domain = request.get_host()
    protocol = request.scheme
    callback_url = f'{protocol}://{domain}/payment/{slug}/{token}/paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['event'] = event
    logger.info(f'Initiating payment for {event.title} by {tempSub.full_name}')
    return render(request, 'payment/payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request, slug, token):
    event = get_object_or_404(Event, slug=slug)
    tempSub = get_object_or_404(TemporaryEventSubmission, uid=token)
    # only accept POST request.
    if request.method == "POST":
        try:
            
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = event.price*100  # Rs. 200
                try:
                    payment_details = razorpay_client.payment.fetch(payment_id)
                    if payment_details["status"] == "authorized" and not payment_details["captured"]:
                        # capture only if not already captured
                        razorpay_client.payment.capture(payment_id, amount)
                        payment_details = razorpay_client.payment.fetch(payment_id)  # refresh
                        
                    
                    data = {
                        'uu_id': tempSub.uu_id,
                        'full_name': tempSub.full_name,
                        'year': tempSub.year,
                        'email': tempSub.email,
                        'user': tempSub.user,
                        'course': tempSub.course,
                        'section': tempSub.section,
                        'event': event,
                    }
                    submission = EventSubmission.objects.create(**data)
                    event.count = event.count + 1
                    event.save()
                    Payment.objects.create(
                        user=tempSub.user,
                        event=event,
                        payment_id=payment_id,
                        gatewate_response=payment_details,
                        amount=amount/100,
                        signature=signature, 
                        order_id=razorpay_order_id,
                        status='COMPLETED'
                    )
                    # render success page on successful caputre of payment
                    messages.success(request, f"Payment Successful for {event.title} event")
                    logger.info(f'Payment successful for {event.title} by {submission.full_name}')
                    tempSub.delete()
                    return redirect('event', slug=slug)
                except Exception as e:
                    print(e)

                    # if there is an error while capturing payment.
                    payment_details = razorpay_client.payment.fetch(payment_id)
                    Payment.objects.create(
                        user=tempSub.user,
                        event=event,
                        payment_id=payment_id,
                        gatewate_response=payment_details,
                        amount=amount/100,
                        signature=signature, 
                        order_id=razorpay_order_id,
                        status='FAILED'
                    )
                    logger.error(f'Payment capture failed for {event.title} by {tempSub.full_name} \nException: {e}')
                    tempSub.delete()
                    messages.error(request, "Payment Failed. Please try again.")
                    return redirect('event', slug=slug)
            else:

                # if signature verification fails.
                print("Signature verification failed")
                tempSub.delete()
                logger.error(f'Payment signature verification failed for {event.title} by {tempSub.full_name}')
                messages.error(request, "Payment Failed. Please try again.")
                return redirect('event', slug=slug)
        except Exception as e:

            # if we don't find the required parameters in POST data
            logger.error(f'Payment processing error for {event.title} by {tempSub.full_name} \nException: {e}')
            messages.error(request, "Payment Failed. Please try again.")
            print(e)
            return redirect('event', slug=slug)
    else:
       # if other than POST request is made.
        logger.error(f'Invalid payment request method for {event.title} by {tempSub.full_name}')
        return redirect('event', slug=slug)
