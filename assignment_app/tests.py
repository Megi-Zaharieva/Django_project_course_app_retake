from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from course_app.models import CreateCourse
from assignment_app.models import Assignment


class AssignmentAppTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.course = CreateCourse.objects.create(title='Test Course', video_url='https://www.youtube.com/watch?v=k5VxfJpzy1Q', type='Math 1', user=self.user)

    def test_create_assignment_view_get(self):
        response = self.client.get(reverse('assignment_app:create_assignment', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/create_assignment/create-assignment.html')

    def test_create_assignment_view_post(self):
        data = {
            'title': 'Test Assignment',
            'description': 'This is a test assignment.',
        }
        response = self.client.post(reverse('assignment_app:create_assignment', args=[self.course.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('assignment_app:view_assignments', args=[self.course.id]))

    def test_view_assignments_view(self):
        assignment = Assignment.objects.create(title='Test Assignment', description='This is a test assignment.',
                                               course=self.course, created_by=self.user)
        response = self.client.get(reverse('assignment_app:view_assignments', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/create_assignment/view-assignments.html')
        self.assertContains(response, 'Test Assignment')
        self.assertContains(response, assignment.title)
        self.assertContains(response, assignment.description)

    def test_delete_assignment_view_get(self):
        assignment = Assignment.objects.create(title='Test Assignment', description='This is a test assignment.', course=self.course, created_by=self.user)
        response = self.client.get(reverse('assignment_app:delete_assignment', args=[self.course.id, assignment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/create_assignment/confirm_delete_assignment.html')

    def test_delete_assignment_view_post(self):
        assignment = Assignment.objects.create(title='Test Assignment', description='This is a test assignment.', course=self.course, created_by=self.user)
        response = self.client.post(reverse('assignment_app:delete_assignment', args=[self.course.id, assignment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('assignment_app:view_assignments', args=[self.course.id]))
