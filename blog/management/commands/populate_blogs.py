from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Blog, BlogCategory, BlogTag
from account.models import User
import random

class Command(BaseCommand):
    help = 'Populate dummy blog data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Events', 'description': 'University events and activities', 'color': '#3b82f6'},
            {'name': 'Academic', 'description': 'Academic news and updates', 'color': '#10b981'},
            {'name': 'Student Life', 'description': 'Campus life and student activities', 'color': '#f59e0b'},
            {'name': 'Technology', 'description': 'Tech news and innovations', 'color': '#8b5cf6'},
            {'name': 'Sports', 'description': 'Sports events and achievements', 'color': '#ef4444'},
        ]
        
        for cat_data in categories_data:
            category, created = BlogCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create tags
        tags_list = ['announcement', 'workshop', 'competition', 'cultural', 'technical', 
                    'placement', 'exam', 'result', 'admission', 'scholarship']
        
        for tag_name in tags_list:
            tag, created = BlogTag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

        # Get or create admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@university.edu',
                password='admin123',
                is_superuser=True,
                is_staff=True
            )

        # Blog posts data
        blog_posts = [
            {
                'title': 'Annual Tech Fest 2024 - Registration Open',
                'content': '<p>We are excited to announce that registration for our Annual Tech Fest 2024 is now open! This year\'s theme is "Innovation for Tomorrow" and we have lined up amazing competitions, workshops, and guest speakers.</p><p>Key highlights include:</p><ul><li>Coding competitions with prizes worth ₹50,000</li><li>Robotics workshop by industry experts</li><li>Startup pitch competition</li><li>Guest lecture by tech industry leaders</li></ul><p>Don\'t miss this opportunity to showcase your skills and learn from the best!</p>',
                'category': 'Events',
                'tags': ['announcement', 'technical', 'competition']
            },
            {
                'title': 'New Scholarship Program for Meritorious Students',
                'content': '<p>The university is pleased to announce a new scholarship program aimed at supporting academically excellent students from economically disadvantaged backgrounds.</p><p>Eligibility criteria:</p><ul><li>Minimum 85% marks in previous semester</li><li>Family income below ₹3 lakhs per annum</li><li>Active participation in extracurricular activities</li></ul><p>Application deadline: March 15, 2024</p>',
                'category': 'Academic',
                'tags': ['scholarship', 'announcement']
            },
            {
                'title': 'Cultural Week 2024 - Celebrating Diversity',
                'content': '<p>Get ready for the most vibrant week of the year! Cultural Week 2024 will showcase the rich diversity of our student community through various performances, exhibitions, and competitions.</p><p>Events include:</p><ul><li>Traditional dance performances</li><li>Music competitions</li><li>Art exhibitions</li><li>Food festival</li><li>Fashion show</li></ul><p>Join us in celebrating the beautiful tapestry of cultures that make our university special.</p>',
                'category': 'Student Life',
                'tags': ['cultural', 'announcement']
            },
            {
                'title': 'Placement Drive Results - Record Breaking Year',
                'content': '<p>We are thrilled to share that this year\'s placement drive has been our most successful yet, with over 95% of eligible students receiving job offers.</p><p>Key statistics:</p><ul><li>250+ companies participated</li><li>Highest package: ₹45 LPA</li><li>Average package: ₹8.5 LPA</li><li>95% placement rate</li></ul><p>Congratulations to all our students and thanks to the placement cell for their excellent work!</p>',
                'category': 'Academic',
                'tags': ['placement', 'result']
            },
            {
                'title': 'Inter-University Sports Championship Victory',
                'content': '<p>Our university team has emerged victorious in the Inter-University Sports Championship, bringing home 15 medals including 6 gold medals!</p><p>Medal winners:</p><ul><li>Athletics: 4 gold, 2 silver</li><li>Swimming: 2 gold, 3 bronze</li><li>Basketball: 1 silver</li><li>Cricket: 1 gold, 2 bronze</li></ul><p>We are incredibly proud of our athletes and their dedication to excellence.</p>',
                'category': 'Sports',
                'tags': ['competition', 'result']
            },
            {
                'title': 'AI and Machine Learning Workshop Series',
                'content': '<p>Join our comprehensive AI and Machine Learning workshop series designed for students who want to dive deep into the world of artificial intelligence.</p><p>Workshop modules:</p><ul><li>Introduction to Python for AI</li><li>Machine Learning fundamentals</li><li>Deep Learning with TensorFlow</li><li>Computer Vision applications</li><li>Natural Language Processing</li></ul><p>Industry experts will guide you through hands-on projects and real-world applications.</p>',
                'category': 'Technology',
                'tags': ['workshop', 'technical']
            },
            {
                'title': 'Semester Exam Schedule Released',
                'content': '<p>The examination schedule for the current semester has been released. Students are advised to check their respective department notice boards and the university website for detailed timetables.</p><p>Important dates:</p><ul><li>Exam registration deadline: April 10, 2024</li><li>Practical exams: April 15-20, 2024</li><li>Theory exams: April 25 - May 15, 2024</li><li>Result declaration: June 1, 2024</li></ul><p>Best of luck to all students!</p>',
                'category': 'Academic',
                'tags': ['exam', 'announcement']
            },
            {
                'title': 'Student Startup Incubation Program Launch',
                'content': '<p>We are launching a new startup incubation program to support student entrepreneurs in turning their innovative ideas into successful businesses.</p><p>Program benefits:</p><ul><li>Seed funding up to ₹5 lakhs</li><li>Mentorship from industry experts</li><li>Co-working space access</li><li>Legal and financial guidance</li><li>Networking opportunities</li></ul><p>Applications are now open for the first cohort starting in July 2024.</p>',
                'category': 'Technology',
                'tags': ['announcement', 'technical']
            }
        ]

        # Create blog posts
        categories = {cat.name: cat for cat in BlogCategory.objects.all()}
        all_tags = list(BlogTag.objects.all())

        for post_data in blog_posts:
            # Check if blog already exists
            if Blog.objects.filter(title=post_data['title']).exists():
                continue
                
            blog = Blog.objects.create(
                title=post_data['title'],
                content=post_data['content'],
                user=admin_user,
                category=categories.get(post_data['category']),
                status='published',
                published_at=timezone.now(),
                is_featured=random.choice([True, False]),
                view_count=random.randint(50, 500)
            )
            
            # Add tags
            post_tags = [tag for tag in all_tags if tag.name in post_data['tags']]
            blog.tags.set(post_tags)
            
            self.stdout.write(f'Created blog: {blog.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated dummy blog data!'))