
from django.db import models
from django.contrib.auth.models import User
from course_app.models import CreateCourse


class Comments(models.Model):
    course = models.ForeignKey(CreateCourse, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_comments = models.TextField(blank=False, null=False, max_length=250)

    def __str__(self):
        return f"Comments by {self.user.username} for {self.course.title}"


class Review(models.Model):

    CHOICE_REVIEW = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]

    course = models.ForeignKey(CreateCourse, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    review_text = models.TextField(blank=True, null=True, max_length=300)
    rating = models.IntegerField(choices=CHOICE_REVIEW)

    def __str__(self):
        return f"Review by {self.user.username} for {self.course.title}"


