from django.shortcuts import render
from django.http import HttpResponse

from courses.models import Course
from instructors.models import Instructor

def index(request):
    courses = Course.objects.order_by('-release_date')[:3]

    context = {
        'courses': courses,
        'difficulty_choices':difficulty_choices,
        'category_choices':category_choices,
        'price_choices':price_choices,

    }

    return render(request, 'pages/index.html', context)

def about(request):
    # Get all instructors
    instructors = Instructor.objects.order_by('-first_name')

    # Get MVP
    mvp_instructors = Instructor.objects.all().filter(is_mvp=True)

    context = {
        'instructors': instructors,
        'mvp_instructors': mvp_instructors
    }

    return render(request, 'pages/about.html', context)