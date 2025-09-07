from django.core.management.base import BaseCommand
from django.utils import timezone
from events.models import Event
from account.models import User 
import random
import faker
Faker = faker.Faker()


class Command(BaseCommand):
    help = 'Populate dummy event data'
    def handle(self, *args, **options):
        for i in range(5):
            data = {
                'title': Faker.sentence(nb_words=6),
                'description': Faker.paragraph(nb_sentences=5),
                'price': random.choice([0, 99, 299, 399, 499, 599]),
                'poster_url': Faker.image_url(),
                'location' : Faker.city(),
                'limit': random.choice([None, 50, 100, 150, 200]),
                'start_date': timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                'end_date': timezone.now() + timezone.timedelta(days=random.randint(31, 60)),
                'last_date_of_registration': timezone.now() + timezone.timedelta(days=random.randint(1, 15)),
                'offers_certification': random.choice([True, False]),
                'organized_by': User.objects.filter(groups__name=['HOST']).first() or User.objects.filter(is_superuser=True).first() or User.objects.create_superuser(
                    username='admin',  password='admin123'),
                'notify' : False,
            }
            event = Event.objects.create(**data)
            self.stdout.write(f'Created event: {event.title}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated dummy event data'))