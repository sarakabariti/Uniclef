from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django_countries.data import COUNTRIES
from datetime import datetime, timedelta
from .forms import PaymentMethodForm, RefundRequestForm

from .models import User, Enrollment, Refund, PaymentMethod, PaymentHistory, Course #,Review

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
    return render(request, 'users/dashboard.html')


def enroll_course(request, course_id):
    if request.method == 'POST':
        # Handle the course enrollment logic here
        # Create an Enrollment object and handle payment

        course = get_object_or_404(Course, id=course_id)
        user = request.user 

        # Create an Enrollment object
        enrollment = Enrollment(course_id=course, user_id=user, enrolled_at=datetime.now(), amount_paid=course.price)

        # Handle payment (add your payment processing logic here)
        payment_form = PaymentMethodForm(request.POST)
        if payment_form.is_valid():
    
            # If the payment is successful (payment_result is True), create a PaymentMethod
            payment_type = payment_form.cleaned_data['payment_type']
            card_number = payment_form.cleaned_data['card_number']
            cardholder_name = payment_form.cleaned_data['cardholder_name']
            expiration_month = payment_form.cleaned_data['expiration_month']
            expiration_year = payment_form.cleaned_data['expiration_year']
            cvv = payment_form.cleaned_data['cvv']

            payment_method = PaymentMethod(
                user_id=user,
                payment_type=payment_type,
                card_number=card_number,
                cardholder_name=cardholder_name,
                expiration_month=expiration_month,
                expiration_year=expiration_year,
                cvv=cvv
            )
            payment_method.save()

            # Create a PaymentHistory record
            payment_history = PaymentHistory(
                user_id=user,
                enrollment_id=enrollment,
                date=datetime.now(),
                amount=course.price,
                status="Success"  # You can customize this based on payment status
            )
            payment_history.save()

            # Update student progress and grant course access

            messages.success(request, 'Successfully enrolled in the course')
            return redirect('dashboard')
        else:
            messages.error(request, 'Payment information is not valid')
    else:
        # Display the course enrollment form

        course = get_object_or_404(Course, id=course_id)
        payment_form = PaymentMethodForm()

        context = {
            'course': course,
            'payment_form': payment_form,
        }
        return render(request, 'courses/course.html', context)
    
def refund_request(request, enrollment_id):
    if request.method == 'POST':
        refund_form = RefundRequestForm(request.POST)
        if refund_form.is_valid():
            user = request.user 
            enrollment = get_object_or_404(Enrollment, id=enrollment_id)

            # Check if the user is the owner of the enrollment
            if enrollment.user_id == user:
                # Check if it's within 3 days of enrollment
                three_days_ago = datetime.now() - timedelta(days=3)
                if enrollment.enrolled_at >= three_days_ago:
                    # Create a Refund object
                    refund = Refund(
                        user_id=user,
                        enrollment_id=enrollment,
                        request_date=datetime.now(),
                        reason=refund_form.cleaned_data['reason'],
                        status="Pending"  # Initial status
                    )
                    refund.save()

                    messages.success(request, 'Refund request submitted successfully.')
                else:
                    messages.error(request, 'You can only request a refund within 3 days of enrollment.')
            else:
                messages.error(request, 'Unauthorized refund request.')
            return redirect('dashboard')
    else:
        refund_form = RefundRequestForm()
        context = {
            'refund_form': refund_form,
        }
        return render(request, 'users/dashboard.html', context)

def payment_history(request):
    user = request.user 
    payment_history = PaymentHistory.objects.filter(user_id=user).order_by('-date')

    context = {
        'payment_history': payment_history,
    }
    return render(request, 'users/payment_history.html', context)