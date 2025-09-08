from django.core.management.base import BaseCommand
from account.models import User , UserExtra
from django.contrib.auth.models import Group
from base.models import Year,Section,Course
import random
import faker
Faker = faker.Faker()


class Command(BaseCommand):
    help=''