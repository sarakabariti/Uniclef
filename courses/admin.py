from django.contrib import admin

from .models import Course

class CourseAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'price', 'release_date', 'instructor')
  list_display_links = ('id', 'title')
  list_filter = ('instructor',)
  search_fields = ('title', 'description', 'difficulty', 'duration', 'price')
  list_per_page = 25

admin.site.register(Course, CourseAdmin)