from django.core.management.base import BaseCommand
from account.models import User , UserExtra
from django.contrib.auth.models import Group
from base.models import Year,Section,Course
import random
import faker
Faker = faker.Faker()


class Command(BaseCommand):
    help = 'Populate dummy user data'
    def handle(self, *args, **options):
        for i in range(5):
            data = {
                'username': Faker.user_name() + str(random.randint(10, 99)),
                'email': Faker.email(),
                'first_name': Faker.first_name(),
                'last_name': Faker.last_name(),
                'password': '123',
            }
            user = User.objects.create_user(**data)
            user.groups.add(Group.objects.get(name='STUDENT'))
            UserExtra.objects.create(
                user=user,
                phone = Faker.random_number(digits=10, fix_len=True),
                course = Course.objects.order_by('?').first().name,
                section = Section.objects.order_by('?').first().section,
                uu_id = 'UU' + str(Faker.random_number(digits=8, fix_len=True)),
                roll_number = Faker.random_number(digits=8, fix_len=True),
                year = Year.objects.order_by('?').first().year,
            )
            self.stdout.write(f'Created user: {user.username}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated dummy user data'))