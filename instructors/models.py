from django.db import models

class Instructor(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=20)
    is_mvp = models.BooleanField(default=False)
    mvp_month = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_mvp:
            # If this instructor is being set as MVP, remove MVP status from all other instructors
            Instructor.objects.filter(mvp_month=self.mvp_month).update(is_mvp=False)
        super(Instructor, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
