from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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
    return render(request, 'courses/search.html')