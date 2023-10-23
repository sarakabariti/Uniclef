from django.contrib import admin

from .models import Instructor


class InstructorAdmin(admin.ModelAdmin):
  list_display = ('id', 'first_name', 'last_name', 'email')
  list_display_links = ('id', 'first_name', 'last_name')
  search_fields = ('first_name', 'last_name')
  list_per_page = 25

admin.site.register(Instructor, InstructorAdmin)