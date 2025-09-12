from django.core.management.base import BaseCommand
from account.models import User , UserExtra
from django.contrib.auth.models import Group
from base.models import Year,Section,Course
from blog.models import BlogCategory
from certificate.models import CertificateFor
import random
import faker
Faker = faker.Faker()


class Command(BaseCommand):
    help='Creating Base Data'
    
    def handle(self,*args,**kwargs):
        groups = ['HOST','COORDINATOR','STUDENT']
        courses = ['BCA','BTECH','BBA','BCOM','MBA','LLB','MTECH','LLB']
        sections = ['A','B','C','D','E']
        years = ['I','II','III','IV','V']
        blog_categories = ['TECH','CULTURAL','SPORTS', 'ACADEMIC', 'EVENT', 'WORKSHOP','OTHER']
        blog_category_colors = ['#FF5733','#33FF57','#3357FF','#F333FF','#33FFF5','#F5FF33','#FF33A8']
        certificate_categories = ['Participation','Second Runner Up','Runner Up','Winner']
        
        for group in groups:
            Group.objects.get_or_create(name=group)
            self.stdout.write(self.style.SUCCESS(f'Group {group} created successfully'))
        for course in courses:
            Course.objects.get_or_create(name=course)
            self.stdout.write(self.style.SUCCESS(f'Course {course} created successfully'))
        for section in sections:
            Section.objects.get_or_create(section=section)
            self.stdout.write(self.style.SUCCESS(f'Section {section} created successfully'))
        for year in years:
            Year.objects.get_or_create(year=year)
            self.stdout.write(self.style.SUCCESS(f'Year {year} created successfully'))
        for i in range(len(certificate_categories)):
            CertificateFor.objects.get_or_create(title=certificate_categories[i])
            self.stdout.write(self.style.SUCCESS(f'Certificate {certificate_categories[i]} created successfully'))
        for i in range(len(blog_categories)):
            BlogCategory.objects.get_or_create(name=blog_categories[i],color=blog_category_colors[i])
            self.stdout.write(self.style.SUCCESS(f'Blog Category {blog_categories[i]} created successfully'))
        self.stdout.write(self.style.SUCCESS('Base Data Created Successfully'))