from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from course_app.models import CreateCourse


class CourseAppTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_add_course_view_get(self):
        response = self.client.get(reverse('course_app:add_course'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/teachers/add-course.html')

    def test_add_course_view_post(self):
        data = {
            'title': 'Test Course',
            'video_url': 'https://www.youtube.com/watch?v=k5VxfJpzy1Q',
            'type': 'Math 1',
            'date': '2023-08-15',
        }
        response = self.client.post(reverse('course_app:add_course'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('course_app:my_courses'))

    def test_course_details_view(self):
        course = CreateCourse.objects.create(title='Test Course', video_url='https://www.youtube.com/watch?v=k5VxfJpzy1Q', type='Math 1', user=self.user)
        response = self.client.get(reverse('course_app:course_details', args=[course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/teachers/course-details.html')
        self.assertContains(response, 'Test Course')

    def test_edit_course_view_get(self):
        course = CreateCourse.objects.create(title='Test Course', video_url='https://www.youtube.com/watch?v=k5VxfJpzy1Q', type='Math 1', user=self.user)
        response = self.client.get(reverse('course_app:edit_course', args=[course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/teachers/course-edit.html')

    def test_edit_course_view_post(self):
        course = CreateCourse.objects.create(title='Test Course', video_url='https://www.youtube.com/watch?v=k5VxfJpzy1Q', type='Math 1', user=self.user)
        data = {
            'title': 'Updated Course',
            'video_url': 'https://www.youtube.com/watch?v=k5VxfJpzy1Q',
            'type': 'Math 2',
        }
        response = self.client.post(reverse('course_app:edit_course', args=[course.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('course_app:course_details', args=[course.id]))

    def test_delete_course_view_get(self):
        course = CreateCourse.objects.create(title='Test Course', video_url='https://www.youtube.com/watch?v=k5VxfJpzy1Q', type='Math 1', user=self.user)
        response = self.client.get(reverse('course_app:delete_course', args=[course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/teachers/course-delete.html')

    def test_delete_course_view_post(self):
        course = CreateCourse.objects.create(title='Test Course', video_url='https://www.youtube.com/watch?v=k5VxfJpzy1Q', type='Math 1', user=self.user)
        response = self.client.post(reverse('course_app:delete_course', args=[course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('course_app:my_courses'))
