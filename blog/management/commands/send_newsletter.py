from django.core.management.base import BaseCommand
from blog.utils import send_newsletter

class Command(BaseCommand):
    help = 'Send newsletter to subscribers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--frequency',
            type=str,
            default='weekly',
            choices=['daily', 'weekly', 'monthly'],
            help='Newsletter frequency'
        )

    def handle(self, *args, **options):
        frequency = options['frequency']
        self.stdout.write(f'Sending {frequency} newsletter...')
        
        send_newsletter(frequency)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {frequency} newsletter!')
        )