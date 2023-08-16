
from django.contrib import admin
from course_app.models import CreateCourse


class CreateCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'user', 'type']
    list_filter = ['date', 'user']
    search_fields = ['title', 'user__username']
    list_per_page = 10
    ordering = ['-date']


admin.site.register(CreateCourse, CreateCourseAdmin)