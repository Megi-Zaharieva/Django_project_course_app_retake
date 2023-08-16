from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from course_app.models import CreateCourse
from search_app.models import SearchModel
from search_app.forms import SearchForm


class SearchAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.course = CreateCourse.objects.create(title='Test Course', video_url='https://www.youtube.com/watch?v=k5VxfJpzy1Q', type='Math 1', user=self.user)

    def test_search_view_get(self):
        response = self.client.get(reverse('search_app:search_results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/comments/search_results.html')
        self.assertIsInstance(response.context['form'], SearchForm)

    def test_search_view_post_valid(self):
        form_data = {'search_text': 'Test'}
        response = self.client.post(reverse('search_app:search_results'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/comments/search_results.html')
        self.assertIsInstance(response.context['form'], SearchForm)
        self.assertTrue(response.context['search_button_clicked'])
        self.assertIn(self.course, response.context['courses_ls'])

    def test_search_view_post_invalid(self):
        form_data = {'search_text': ''}
        response = self.client.post(reverse('search_app:search_results'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic_app/comments/search_results.html')
        self.assertIsInstance(response.context['form'], SearchForm)
        self.assertFalse(response.context['search_button_clicked'])

    def test_search_model_creation(self):
        search_text = 'Test Search'
        SearchModel.objects.create(search_text=search_text)
        self.assertEqual(SearchModel.objects.count(), 1)
        search_model = SearchModel.objects.first()
        self.assertEqual(search_model.search_text, search_text)

    def test_search_form_valid(self):
        form = SearchForm(data={'search_text': 'Test'})
        self.assertTrue(form.is_valid())

    def test_search_form_invalid(self):
        form = SearchForm(data={'search_text': ''})
        self.assertFalse(form.is_valid())


