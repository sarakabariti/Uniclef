from django.db import models
from datetime import datetime
from instructors.models import Instructor

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
    release_date = models.DateTimeField(default=datetime.now, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
