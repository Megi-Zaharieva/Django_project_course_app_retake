from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from base_app.models import UserProfileInfo
from base_app.forms import UserForm, UserProfileInfoForm
from base_app.validators import PasswordInfo


class BaseAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = UserProfileInfo.objects.create(user=self.user, type='Student')

    def test_password_info_help_text(self):
        password_info = PasswordInfo().get_help_text()
        self.assertIn('at least', password_info)
        self.assertIn('1 letter', password_info)
        self.assertIn('1 digit', password_info)

    def test_user_form_valid_data(self):
        form = UserForm(data={
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': '1q2w3e4r5t*'
        })
        self.assertTrue(form.is_valid())

    def test_user_profile_form_valid_data(self):
        form = UserProfileInfoForm(data={
            'type': 'Teacher'
        })
        self.assertTrue(form.is_valid())

    def test_index_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('base_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, testuser")

    def test_index_view_anonymous_user(self):
        response = self.client.get(reverse('base_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Perennial course in mathematics')

    def test_user_register_view_get(self):
        response = self.client.get(reverse('base_app:registration'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please Register')



