from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event,EventSubmission
from account.models import User 
import random
import faker
Faker = faker.Faker()


class Command(BaseCommand):
    help = 'Populate dummy event registration!'
    def handle(self, *args, **options):
        for i in range(10):
            event = Event.objects.filter(event_open=True,registration_open=True,event_over = False,status='approved').order_by('?').first()
            user = User.objects.filter(is_active=True).order_by('?').first()
            if int(event.count) < int(event.limit):
                if not EventSubmission.objects.filter(user=user,event=event).exists():
                    submission = EventSubmission.objects.create(
                        user=user,
                        event=event,
                        attendence=random.choice(['Present', 'Absent']),
                        uu_id = user.user_extra.uu_id if user.user_extra.uu_id else '',
                        full_name = user.get_full_name(),
                        email = user.email,
                        course = user.user_extra.course if user.user_extra.course else '',
                        section = user.user_extra.section if user.user_extra.section else '',
                        year = user.user_extra.year if user.user_extra.year else '',
                    )
                    self.stdout.write(f'User {user.username} registered for event: {event.title}')
                else:
                    self.stdout.write(f'User {user.username} already registered for event: {event.title}')
            else:
                self.stdout.write(f'Event {event.title} has reached its limit.')
            self.stdout.write(self.style.SUCCESS('Successfully populated dummy event registrations!'))