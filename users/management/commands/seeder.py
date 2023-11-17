import random
from django_seed import Seed
from django.core.management.base import BaseCommand
from instructors.models import Instructor
from courses.models import Category, Course, CourseCategory
from users.models import User, Enrollment, Refund, PaymentMethod
from django.contrib.auth.models import Group, Permission, ContentType
from django_countries import countries
from django.utils import timezone

class Command(BaseCommand):
    help = "This command seeds the database"

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        # Seed Instructor
        seeder.add_entity(Instructor, 3, {
            'first_name': lambda x: seeder.faker.first_name(),
            'last_name': lambda x: seeder.faker.last_name(),
            'photo': None,
            'description': lambda x: seeder.faker.text(),
            'email': lambda x: seeder.faker.email(),
            'phone_number': lambda x: seeder.faker.phone_number(),
            'is_mvp': False,
            'mvp_month': lambda x: random.choice([None, None, None, seeder.faker.date_this_year(None)]),
        })
        '''
        # Seed Category
        seeder.add_entity(Category, 5, {
            'category_tag': lambda x: seeder.faker.word(),
            'description': lambda x: seeder.faker.text(),
        })
        inserted_categories = seeder.execute()

        # Seed Course
        seeder.add_entity(Course, 10, {
            'title': lambda x: seeder.faker.sentence(nb_words=5),
            'description': lambda x: seeder.faker.text(),
            'difficulty': lambda x: random.choice(['beginner', 'intermediate', 'advanced']),
            'duration': lambda x: random.randint(1, 25),
            'photo': None, 
            'instructor': lambda x: random.choice(Instructor.objects.all()),
            'release_date': lambda x: seeder.faker.date_time_this_year(),
            'price': lambda x: round(random.uniform(15, 100), 2),
            'category': lambda x: random.choice(Category.objects.all()),
        })
        inserted_courses = seeder.execute()

        # Seed CourseCategory
        for course_id in inserted_courses[Course]:
            course = Course.objects.get(pk=course_id)
            categories = seeder.sample(Category.objects.all(), 2)
            for category in categories:
                seeder.add_entity(CourseCategory, 1, {
                    'course': course,
                    'category': category,
                })
        ''' 
        # Seed Group
        seeder.add_entity(Group, 5, {
            'name': lambda x: seeder.faker.word(),
        })
        inserted_groups = seeder.execute()

        # Seed Permission
        seeder.add_entity(Permission, 5, {
            'name': lambda x: seeder.faker.word(),
            'content_type': lambda x: random.choice(ContentType.objects.all()),
        })
        inserted_permissions = seeder.execute()  
        # Seed User
        seeder.add_entity(User, 10, {
            'first_name': lambda x: seeder.faker.first_name(),
            'last_name': lambda x: seeder.faker.last_name(),
            'email': lambda x: seeder.faker.email(),
            'phone_number': lambda x: seeder.faker.phone_number(),
            'gender': lambda x: random.choice(['male', 'female', 'other']),
            'city': lambda x: seeder.faker.city(),
            'country_code': lambda x: random.choice(list(countries)),
            'profile_pic': None, 
            'date_joined': lambda x: timezone.now(),
            'last_active': lambda x: timezone.now(),
            'is_staff': lambda x: seeder.faker.boolean(),
            'is_active': lambda x: seeder.faker.boolean(),
            'groups': lambda x: random.choice(Group.objects.all()),
            'user_permissions': lambda x: random.choice(Permission.objects.all()),
        })
        inserted_users = seeder.execute()   
            
        # Seed PaymentMethod
        seeder.add_entity(PaymentMethod, 10, {
            'user_id': lambda x: random.choice(User.objects.all()),
            'payment_type': lambda x: random.choice(['credit', 'debit']),
            'card_number': lambda x: seeder.faker.credit_card_number(),
            'cardholder_name': lambda x: seeder.faker.name(),
            'expiration_month': lambda x: random.randint(1, 12),
            'expiration_year': lambda x: random.randint(2023, 2030),
        })
        inserted_payment_methods = seeder.execute()

        # Seed Enrollment
        seeder.add_entity(Enrollment, 20, {
            'course_id': lambda x: random.choice(Course.objects.all()),
            'user_id': lambda x: random.choice(User.objects.all()),
            'enrolled_at': lambda x: timezone.now(),
            'amount_paid': lambda x: round(random.uniform(15, 100), 2),
            'payment_method_id': lambda x: random.choice(PaymentMethod.objects.all()),
            'refunded': lambda x: seeder.faker.boolean(),
        })
        inserted_enrollments = seeder.execute()

        # Seed Refund
        seeder.add_entity(Refund, 5, {
            'enrollment_id': lambda x: random.choice(Enrollment.objects.all()),
            'request_date': lambda x: timezone.now(),
            'reason': lambda x: seeder.faker.text(),
            'status': lambda x: random.choice(['pending', 'rejected']),
        })
                

        seeder.execute()

        self.stdout.write(self.style.SUCCESS('Database seeded!'))