from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django_countries.data import COUNTRIES
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from .models import User, Enrollment, Refund, PaymentMethod, Course #,Review

import stripe
import json

def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        gender = request.POST['gender']
        city = request.POST['city']
        country_code = request.POST['country_code']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match:
        if password == password2:
            # Check email
            if User.objects.filter(email=email).exists():
                messages.error(request, 'There is already an account registered with that email')
                return redirect('register')
            else:
                # Validate email
                try:
                    EmailValidator()(email)
                except ValidationError as e:
                    messages.error(request, e.messages[0])
                    return redirect('register')
                
                # Validate password
                try:
                    validate_password(password)
                except ValidationError as e:
                    messages.error(request, e.messages[0])
                    return redirect('register')

                # Check if password is same as email
                if password == email:
                    messages.error(request, 'Password cannot be the same as the email')
                    return redirect('register')
                
                # Fetch the selected country using country_code
                country = COUNTRIES.get(country_code)
                if country:
                # Create user
                    user = User.objects.create_user(
                        email=email,
                        first_name=first_name, 
                        last_name=last_name, 
                        phone_number=phone_number,
                        gender=gender, 
                        city=city, 
                        country_code=country_code,
                        password=password)
                    # Login after register
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in')
                    return redirect('index')
                else:
                    messages.error(request, 'Invalid country code')
                    return redirect('register')
            
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        # Retrieve the list of countries directly from django-countries
        countries = COUNTRIES
        context = {
            'countries': countries,
            'password_help_texts': password_validators_help_texts(),
        }
        return render(request, 'users/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid creditentials")
            return redirect('login')
    else:
        return render(request, 'users/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return redirect('index')

def dashboard(request):
    # Display enrolled courses on the dashboard
    if request.user.is_authenticated:
        enrollments = Enrollment.objects.filter(user_id=request.user.id)
        enrolled_courses = [enrollment.course_id for enrollment in enrollments]
        return render(request, 'users/dashboard.html', {'enrolled_courses': enrolled_courses})
    else:
        return redirect('login')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the payment_intent.succeeded event
    if event['type'] == 'payment_intent.succeeded':
        print('Payment was successful!')

    return HttpResponse(status=200)


import logging

logger = logging.getLogger(__name__)

# Decorator to ensure that the view is accessible only by authenticated users
@login_required
@csrf_exempt
def enroll_and_pay(request):
    if request.method == 'POST':
        course_id = request.POST['course_id']
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # Check if the user is already enrolled in the course
        if Enrollment.objects.filter(course_id=course_id, user_id=user.id).exists():
            messages.error(request, 'You are already enrolled in this course.')
            return HttpResponseRedirect(reverse('dashboard'))
        
        # Retrieve the payment token from the client-side
        token = request.POST['stripe_token']

        try:
            # Set Stripe API key
            stripe.api_key = settings.STRIPE_SECRET_KEY
            

            # Create a PaymentIntent using the Stripe API
            payment_intent = stripe.PaymentIntent.create(
                amount=int(course.price * 100),  # Convert to cents
                currency='usd',
                description=f'Payment for Course: {course.title}',
                confirm=True,
                payment_method_data={
                    'type': 'card',
                    'card': {'token': token}
                },
                automatic_payment_methods={
                'enabled': True,
                'allow_redirects': 'never'
                }            
            )
            logger.info(f'PaymentIntent created: {payment_intent}')

            # If the charge is successful, create the paymentmethod and enrollment records
            if payment_intent.status == 'succeeded':
                # Fetch the charges associated with the payment_intent
                charges = stripe.Charge.list(payment_intent=payment_intent.id)
                # Access the first charge
                charge = charges.data[0]
                payment_method = PaymentMethod.objects.create(
                    user_id=user,
                    payment_type='card',
                    card_number=charge.payment_method_details.card.last4,
                    cardholder_name=request.POST['cardholder_name'],
                    expiration_month=charge.payment_method_details.card.exp_month,
                    expiration_year=charge.payment_method_details.card.exp_year,
                )

                enrollment = Enrollment.objects.create(
                    course_id=course,
                    user_id=user,
                    enrolled_at=timezone.now(),
                    amount_paid=course.price, 
                    payment_method_id=payment_method,
                    refunded=False
                )

                # Return a success response to the client
                return JsonResponse({'success': True, 'message': 'Payment successful'})
            else:
                logger.info('Payment failed')
                return JsonResponse({'success': False, 'message': 'Payment failed'})
                
        except stripe.error.CardError:
            logger.exception('Card error')
            return JsonResponse({'error': 'Payment failed. Please check your card information.'})
        except Exception as e:
            logger.exception('An error occurred')
            return JsonResponse({'error': 'An error occurred. Please contact support.'})

    return render(request, 'courses/course.html', {'course': course})

def refund_request(request):
    if request.method == 'POST':
        enrollment_id = request.POST['enrollment_id']
        reason = request.POST['message']

        course = get_object_or_404(Course, id=request.POST['course_id'])

        try:
            enrollment_id = int(enrollment_id)
        except (ValueError, TypeError):
            # Handle the case where enrollment_id is not a valid integer
            messages.error(request, 'Invalid enrollment ID.')
            return redirect('dashboard')

        # Check if the user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to request a refund.')
            return redirect('login')
        
        # Check if user already made a refund request
        has_requested = Refund.objects.filter(enrollment_id=enrollment_id).exists()
        if has_requested:
            messages.error(request, 'You already made a refund request.')
            return redirect(reverse('course', args=[course.id]))

        # Fetch the enrollment, if it exists
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, user_id=request.user.id, course_id=request.course.id)
        except Enrollment.DoesNotExist:
            messages.error(request, 'You are not enrolled in this course.')
            return redirect('dashboard')  

        # Check if it's within 3 days of enrollment
        three_days_ago = datetime.now() - timedelta(days=3)
        if enrollment.enrolled_at >= three_days_ago:
            # Create a Refund object
            refund = Refund(
                enrollment_id=enrollment,
                request_date=timezone.now(),
                reason=reason,
                status="Pending"  # Initial status
            )
            refund.save()

            messages.success(request, 'Refund request submitted successfully.')
        else:
            messages.error(request, 'You can only request a refund within 3 days of enrollment.')

        return redirect(reverse('course', args=[course.id]))

    return redirect('dashboard') 

def payment_history(request):
    if request.user.is_authenticated:
        payment_history = Enrollment.objects.filter(user_id=request.user.id).values(
            'course_id__title', 
            'enrolled_at', 
            'amount_paid', 
            'payment_method_id__payment_type', 
            'payment_method_id__card_number').order_by('-enrolled_at')
        return render(request, 'users/payment_history.html', {'payment_history': payment_history})
    else:
        return redirect('login')
    

    