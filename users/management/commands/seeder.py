import random
import json
from django_seed import Seed
from django.core.management.base import BaseCommand
from instructors.models import Instructor
from courses.models import Category, Course, CourseCategory
from users.models import User, Enrollment, Refund, PaymentMethod
from django.contrib.auth.models import Group, Permission, ContentType
from django_countries import countries
from django.utils import timezone
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "This command seeds the database"

    def handle(self, *args, **options):
        # Generate fake data for Instructor
        instructors_data = []
        last_pk_instructor =  Instructor.objects.last().id if Instructor.objects.exists() else 0
        for _ in range(3):
            last_pk_instructor += 1
            instructor_data = {
                'model': 'instructors.instructor',
                'pk': last_pk_instructor,
                'fields': {
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'photo': fake.image_url(),
                    'description': fake.text(),
                    'email': fake.email(),
                    'phone_number': fake.phone_number(),
                    'is_mvp': False,
                    'mvp_month': None if random.choice([True, False]) else fake.date_this_year().isoformat(),
                }
            }
            instructors_data.append(instructor_data)
        # Save fake data to JSON file
        with open('instructors_data.json', 'w') as f:
            json.dump(instructors_data, f, indent=2)
        
        # Generate fake data for Category
        categories_data = []
        last_pk_category =  Category.objects.last().id if Category.objects.exists() else 0
        for _ in range(3):
            last_pk_category += 1
            category_data = {
                'model': 'courses.category',
                'pk': last_pk_category,	
                'fields': {
                    'category_tag': fake.word(),
                    'description': fake.text(),
                }
            }
            categories_data.append(category_data)
        # Save fake data to JSON file
        with open('categories_data.json', 'w') as f:
            json.dump(categories_data, f, indent=2)

        # Generate fake data for Course and CourseCategory
        courses_data = []
        course_categories_data = []
        course_category_combinations = set()  # This set will store the (course_id, category_id) combinations
        last_pk_course = Course.objects.last().id if Course.objects.exists() else 0
        last_pk_course_category = CourseCategory.objects.last().id if CourseCategory.objects.exists() else 0
        for _ in range(3):
            last_pk_course += 1
            course_data = {
                'model': 'courses.course',
                'pk': last_pk_course,
                'fields': {
                    'title': fake.sentence(nb_words=5),
                    'description': fake.text(),
                    'difficulty': random.choice(['beginner', 'intermediate', 'advanced']),
                    'duration': random.randint(1, 25),
                    'photo': fake.image_url(),
                    'instructor': random.choice(list(Instructor.objects.all())).id,
                    'release_date': timezone.make_aware(fake.date_time_this_year()).isoformat(),
                    'price': round(random.uniform(15, 100), 2),
                }
            }
            courses_data.append(course_data)

            # Generate fake data for CourseCategory
            num_categories = random.randint(1, 3)  # Generate a random number of categories to associate with the course
            # Get a list of Category instances
            categories = list(Category.objects.all())
            # Get a list of their 'id' attribute
            category_ids = [category.id for category in categories]
            # Select a random sample of 'id' attributes
            selected_categories = random.sample(category_ids, num_categories)
                      
            for category in selected_categories:
                course_id = random.choice(list(Course.objects.all())).id
                # Check if the combination is already in the set
                if (course_id, category) in course_category_combinations:
                    continue #If it is, then skip it
                course_category_combinations.add((course_id, category))
                last_pk_course_category += 1
                course_category_data = {
                    'model': 'courses.coursecategory',
                    'pk': last_pk_course_category,
                    'fields': {
                        'course_id':random.choice(list(Course.objects.all())).id,
                        'category_id': category,
                    }
                }
                course_categories_data.append(course_category_data)
        # Save fake data to JSON file
        with open('courses_data.json', 'w') as f:
            json.dump(courses_data, f, indent=2)
        with open('course_categories_data.json', 'w') as f:
            json.dump(course_categories_data, f, indent=2)

       
        # Generate fake data for User
        users_data = []
        generated_emails = set()
        last_pk_user = User.objects.last().id if User.objects.exists() else 0
        for _ in range(5):
            last_pk_user += 1
            email = fake.email()
            while email in generated_emails:  # Keep generating a new email until it's unique
                email = fake.email()
            generated_emails.add(email)
            user_data = {
                'model': 'users.user',
                'pk': last_pk_user,
                'fields': {
                    'password': fake.password(),
                    'last_login': timezone.make_aware(fake.date_time_this_year()).isoformat(),
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': email,
                    'phone_number':fake.phone_number()[:20],
                    'gender':random.choice(['male', 'female', 'other']),
                    'city':fake.city(),
                    'country_code':random.choice(list(countries)).code,
                    'profile_pic':fake.image_url(),
                    'date_joined': timezone.make_aware(fake.date_time_this_year()).isoformat(),
                    'last_active': timezone.make_aware(fake.date_time_this_year()).isoformat(),
                    'is_staff':fake.boolean(),
                    'is_active':fake.boolean(),
                }
            }
            users_data.append(user_data)
        # Save fake data to JSON file
        with open('users_data.json', 'w') as f:
            json.dump(users_data, f, indent=2)

        # Generate fake data for PaymentMethod
        payments_data = []
        last_pk_payment = PaymentMethod.objects.last().id if PaymentMethod.objects.exists() else 0
        for _ in range(2):
            last_pk_payment += 1
            payment_data = {
                'model': 'users.paymentmethod',
                'pk': last_pk_payment,
                'fields': {
                    'user_id' : random.choice(list(User.objects.all())).id,
                    'payment_type': random.choice(['credit', 'debit']),
                    'card_number': fake.credit_card_number(),
                    'cardholder_name': fake.name(),
                    'expiration_month': random.randint(1, 12),
                    'expiration_year': random.randint(2023, 2030),
                }
            }
            payments_data.append(payment_data)
        # Save fake data to JSON file
        with open('payments_data.json', 'w') as f:
            json.dump(payments_data, f, indent=2)

        # Generate fake data for Enrollment
        enrollments_data = []
        enrollment_combinations = set()  # This set will store the (course_id, user_id) combinations
        last_pk_enrollment = Enrollment.objects.last().id if Enrollment.objects.exists() else 0
        for _ in range(5):
            last_pk_enrollment += 1
            course_id = random.choice(list(Course.objects.all())).id
            user_id = random.choice(list(User.objects.all())).id
            # Check if the combination is already in the set
            if (course_id, user_id) in enrollment_combinations:
                continue  # If it is, skip this iteration
            enrollment_combinations.add((course_id, user_id))  # Otherwise, add it to the set
            
            enrollment_data = {
                'model': 'users.enrollment',
                'pk': last_pk_enrollment,
                'fields': {
                    'course_id': course_id,
                    'user_id': user_id,
                    'enrolled_at': timezone.make_aware(fake.date_time_this_year()).isoformat(),
                    'amount_paid': round(random.uniform(15, 100), 2),
                    'payment_method_id': random.choice(list(PaymentMethod.objects.all())).id,
                    'refunded': fake.boolean(),
                }
            }
            enrollments_data.append(enrollment_data)
        # Save fake data to JSON file
        with open('enrollments_data.json', 'w') as f:
            json.dump(enrollments_data, f, indent=2)

        # Generate fake data for Refund
        refunds_data = []
        # Get a list of all 'enrollment_id's that are not in the refund table
        enrollment_ids = list(Enrollment.objects.exclude(id__in=Refund.objects.values_list('enrollment_id', flat=True)).values_list('id', flat=True))
        last_pk_refund = Refund.objects.last().id if Refund.objects.exists() else 0
        # If there are no such 'enrollment_id's, then skip the refund data generation
        if not enrollment_ids:
            self.stdout.write(self.style.WARNING('No new enrollments for refunds. Skipping refund data generation.'))
        else:

            for _ in range(3):
                # Check if there are still enrollment_ids left
                if not enrollment_ids:
                    break
                last_pk_refund += 1
                # Select a random 'enrollment_id' from the list
                enrollment_id = random.choice(enrollment_ids)
                # Remove the selected 'enrollment_id' from the list
                enrollment_ids.remove(enrollment_id)

                refund_data = {
                    'model': 'users.refund',
                    'pk': last_pk_refund,
                    'fields': {
                        'enrollment_id': enrollment_id,
                        'request_date': timezone.make_aware(fake.date_time_this_year()).isoformat(),
                        'reason': fake.text(),
                        'status': random.choice(['pending', 'rejected']),
                    }
                }
                refunds_data.append(refund_data)

        # Save fake data to JSON file
        with open('refunds_data.json', 'w') as f:
            json.dump(refunds_data, f, indent=2)

        self.stdout.write(self.style.SUCCESS('Database seeded!'))