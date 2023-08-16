from django.contrib import admin
from .models import Assignment


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_by', 'created_at')
    list_filter = ('course', 'created_by')


admin.site.register(Assignment, AssignmentAdmin)
