from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

User_model = get_user_model()


class UserProfileInfo(models.Model):
    CHOICES = [
        ('Teacher', 'Teacher'),
        ('Student', 'Student')
    ]
    APPROVE_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, max_length=800)
    type = models.CharField(blank=False, null=False, choices=CHOICES)
    file = models.FileField(blank=True, null=True, upload_to='user_files')
    admin_approved = models.CharField(blank=True, null=True, choices=APPROVE_CHOICES)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True,)

    def __str__(self):
        return self.user.username


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_pic', 'file', 'type', 'admin_approved']
    fields = ['user', 'profile_pic', 'file', 'type', 'admin_approved']