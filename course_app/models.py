
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CreateCourse(models.Model):

    CHOICES = [
        ('Math 1', 'Math 1'),
        ('Math 2', 'Math 2'),
        ('Math 3', 'Math 3'),
        ('Math 4', 'Math 4'),
        ('Math 5', 'Math 5'),
        ('Math 6', 'Math 6'),
        ('Math 7', 'Math 7'),
        ('Math 8', 'Math 8'),
        ('Math 9', 'Math 9'),
        ('Math 10', 'Math 10'),
        ('Math 11', 'Math 11'),
        ('Math 12', 'Math 12')
    ]

    title = models.CharField(blank=False, null=False, max_length=255)
    video_url = models.URLField(default=None)
    course_image_url = models.URLField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(blank=False, null=False, choices=CHOICES)
    description = models.TextField(blank=True, null=True, max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title