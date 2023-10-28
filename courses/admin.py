from django.contrib import admin

from .models import Course, Category, CourseCategory

# Define a function to get the category names for a course
def get_category_names(obj):
    return ", ".join([category.category_tag for category in obj.category.all()])

class CourseCategoryInline(admin.TabularInline):
    model = CourseCategory
    extra = 1  # Adjust the number of inline forms as needed

class CourseAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', get_category_names, 'price', 'release_date', 'instructor')
  list_display_links = ('id', 'title')
  list_filter = ('instructor',)
  search_fields = ('title', 'description', 'difficulty', 'duration', 'price')
  list_per_page = 25
  inlines = [CourseCategoryInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_tag', 'description')
    list_display_links = ('id', 'category_tag')

admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)