from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django_countries.data import COUNTRIES

from .models import User

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
        # Login User
        return
    else:
        return render(request, 'users/login.html')

def logout(request):
    return redirect('index')

def dashboard(request):
    return render(request, 'users/dashboard.html')
