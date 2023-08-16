
from django.contrib import admin
from base_app.models import UserProfileInfo


class UserProfileInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_pic', 'type', 'admin_approved']
    list_filter = ['type', 'admin_approved']
    search_fields = ['user__username']


admin.site.register(UserProfileInfo, UserProfileInfoAdmin)