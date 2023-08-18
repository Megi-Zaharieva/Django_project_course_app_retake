from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from base_app.validators import validate_youtube_url


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
    video_url = models.URLField(default=None, validators=[validate_youtube_url])
    course_image = models.ImageField(upload_to='profile_pics', blank=True, )
    image_url = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(blank=False, null=False, choices=CHOICES)
    description = models.TextField(blank=True, null=True, max_length=800)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

