import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from events.models import Event
from django.utils import timezone
import json

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')

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
                    context += f"- {event.title} ({event.start_date.strftime('%b %d')} - {event.end_date.strftime('%b %d')}): Price (in rupee): {event.price if event.price else 'Free'}\n"
                context += "\n"
            
            if upcoming_events.exists():
                context += "Upcoming Events:\n"
                for event in upcoming_events:
                    context += f"- {event.title} (starts {event.start_date.strftime('%b %d, %Y')}): Price (in rupee): {event.price if event.price else 'Free'}\n"
            
            # Generate response using Gemini
            response = model.generate_content(f"""
            You are a helpful assistant for Event Niti, a university event management system.
            Keep responses concise and friendly. Help with event-related queries.
            
            Context:
            {context}
            
            User: {user_message}
            """)
            
            return JsonResponse({
                'success': True,
                'response': response.text
            })
            
        except Exception as e:
            print(e)
            return JsonResponse({
                'success': False,
                'response': 'Sorry, I encountered an error. Please try again.'
            })
    
    return JsonResponse({'success': False, 'response': 'Invalid request'})
