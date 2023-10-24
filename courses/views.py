from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, category_choices, difficulty_choices

from .models import Course

def index(request):
    courses = Course.objects.order_by('-release_date')

    paginator = Paginator(courses, 3)
    page = request.GET.get('page')
    paged_courses = paginator.get_page(page)

    context = {
        'courses':paged_courses
    }
    return render(request, 'courses/courses.html', context)

def course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    context = {
    'course': course
    }
    return render(request, 'courses/course.html', context)

def search(request):
    queryset_list = Course.objects.order_by('-release_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # Duration
    if 'duration' in request.GET:
        duration = request.GET['duration']
        if duration:
            queryset_list = queryset_list.filter(duration__lte=duration)
    
    # Difficulty
    if 'difficulty' in request.GET:
        difficulty = request.GET['diffuclty']
        if difficulty:
            queryset_list = queryset_list.filter(difficulty__iexact=difficulty)

    # Category
    if 'category' in request.GET:
        category = request.GET['category']
        if category:
            queryset_list = queryset_list.filter(category__iexact=category)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
    
    context = {
    'difficulty_choices': difficulty_choices,
    'category_choices': category_choices,
    'price_choices': price_choices,
    'courses': queryset_list,
    'values': request.GET
    }

    return render(request, 'courses/search.html', context)