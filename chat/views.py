import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from events.models import Event
from django.utils import timezone
from django.utils.safestring import mark_safe
import json
import re
import logging 
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def format_bold(text):
    # Replace **word** with <b>word</b>
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return mark_safe(text)  


@csrf_exempt
def chat_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            current_page = data.get('page', 'unknown')
            
            # Get approved ongoing and upcoming events
            now = timezone.now()
            ongoing_events = Event.objects.filter(
                status='approved',
                start_date__lte=now,
                end_date__gte=now
            )[:5]
            
            upcoming_events = Event.objects.filter(
                status='approved',
                start_date__gt=now
            ).order_by('start_date')[:5]
            
            # Build context
            context = f"Current page: {current_page}\n\n"
            
            if ongoing_events.exists():
                context += "Ongoing Events:\n"
                for event in ongoing_events:
                    context += f"""
                       [
                        Title : {event.title} \n
                        Description : {mark_safe(event.description)} \n
                        Start Date : ({event.start_date.strftime('%b %d')}  \n
                        End Date : {event.end_date.strftime('%b %d')}) \n
                        Registration Last Date : {event.last_date_of_registration.strftime('%b %d') if event.last_date_of_registration else ''}) \n
                        Price : {event.price if event.price else 'Free'} \n
                        organized_by : {event.organized_by.get_full_name()} \n 
                        Organizer Phone : {event.organized_by.user_extra.phone} \n
                        Organizer Email : {event.organized_by.email} \n
                        venue : {event.location}\n
                        offers_certification : {'Yes' if event.offers_certification else 'No'}\n
                       ] \n
                        """
                context += "\n"
            
            if upcoming_events.exists():
                context += "Upcoming Events:\n"
                for event in upcoming_events:
                    context += f"""
                       [
                        Title : {event.title} \n
                        Description : {mark_safe(event.description)} \n
                        Start Date : ({event.start_date.strftime('%b %d')}  \n
                        End Date : {event.end_date.strftime('%b %d')}) \n
                        Registration Last Date : {event.last_date_of_registration.strftime('%b %d') if event.last_date_of_registration else ''}) \n
                        Price : {event.price if event.price else 'Free'} \n
                        organized_by : {event.organized_by.get_full_name()} \n 
                        Organizer Phone : {event.organized_by.user_extra.phone} \n
                        Organizer Email : {event.organized_by.email} \n
                        venue : {event.location}\n
                        offers_certification : {'Yes' if event.offers_certification else 'No'}\n
                       ] \n
                        """
            
            # Generate response using Gemini
            response = model.generate_content(f"""
            You are a helpful assistant for Event Niti, a university event hosting and management platform.
            Keep responses concise and friendly with excitement tone and with humour. Help with event-related queries.
            
            Context:
            {context}
            
            User: {user_message}
            """)
            logger.info(f"Chat response generated for: {request.user}")
            return JsonResponse({
                'success': True,
                'response': format_bold(response.text)
            })
            
        except Exception as e:
            logger.error(f"Error in chat_response: {e}")
            return JsonResponse({
                'success': False,
                'response': 'Sorry, I encountered an error. Please try again.'
            })
    
    return JsonResponse({'success': False, 'response': 'Invalid request'})
