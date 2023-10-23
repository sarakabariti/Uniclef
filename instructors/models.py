from django.db import models

class Instructor(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    description = models.TextField(blank=True)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=20)
    is_mvp = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
