from django.contrib import admin
from teacher_app.models import Comments, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating']
    list_filter = ['user', 'course', 'rating']
    search_fields = ['user__username', 'course__title', 'review_text']
    list_per_page = 10
    ordering = ['-id']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'user_comments']
    list_filter = ['user', 'course']
    search_fields = ['user__username', 'course__title', 'user_comments']
    list_per_page = 10
    ordering = ['-id']


admin.site.register(Comments, CommentsAdmin)
admin.site.register(Review, ReviewAdmin)

