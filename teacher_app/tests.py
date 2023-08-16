from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from teacher_app.models import CreateCourse, Comments, Review
from teacher_app.forms import CommentsForm, ReviewForm

class TeachersAppTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = CreateCourse.objects.create(
            title='Test Course', user=self.user, video_url='https://www.youtube.com/watch?v=k5VxfJpzy1Q'
        )
        self.comment = Comments.objects.create(course=self.course, user=self.user, user_comments='This is a comment.')
        self.review = Review.objects.create(course=self.course, user=self.user, review_text='This is a review.', rating=4)

    def test_add_comment_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('teacher_app:add_comment', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/comments/add_edit_comment.html')
        self.assertIsInstance(response.context['form'], CommentsForm)

    def test_edit_comment_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('teacher_app:edit_comment', args=[self.course.id, self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/comments/add_edit_comment.html')
        self.assertIsInstance(response.context['form'], CommentsForm)

    def test_delete_comment_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('teacher_app:delete_comment', args=[self.course.id, self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/comments/delete_comment.html')

    def test_add_review_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('teacher_app:add_review', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/comments/add_review.html')
        self.assertIsInstance(response.context['form'], ReviewForm)

    def test_view_reviews_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('teacher_app:view_reviews', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/comments/view_reviews.html')
        self.assertContains(response, 'This is a review.')
