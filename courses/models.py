from django.db import models
from django.utils import timezone
from instructors.models import Instructor

class Category(models.Model):
    category_tag = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_tag
    
class Course(models.Model):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration = models.PositiveIntegerField()  # Duration in weeks
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')  
    instructor = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING)  
    release_date = models.DateTimeField(default=timezone.now, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField(Category, through='CourseCategory')

    def __str__(self):
        return self.title


class CourseCategory(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title} - {self.category.category_tag}"