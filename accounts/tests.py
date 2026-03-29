from django.test import TestCase
from django.urls import reverse
from .models import User
from .forms import RegisterForm

class SignupTests(TestCase):
    def test_register_form_valid(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'organizer',
            'password1': 'pass123456',
            'password2': 'pass123456',
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_json())
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.role, 'organizer')
        self.assertTrue(user.check_password('pass123456'))

    def test_register_form_invalid_password(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': 'participant',
            'password1': 'pass123',
            'password2': 'pass456',
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_success(self):

        data = {
            'username': 'postuser',
            'email': 'post@example.com',
            'first_name': 'Post',
            'last_name': 'User',
            'role': 'judge',
            'password1': 'securepass123',
            'password2': 'securepass123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        user = User.objects.get(username='postuser')
        self.assertEqual(user.role, 'judge')

    def test_role_retainment_on_error(self):
        # Post with error but role selected
        data = {
            'username': 'erroruser',
            'role': 'organizer',
            'password1': 'pass1',
            'password2': 'pass2',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        # Check if organizer is 'checked' in the response content
        self.assertContains(response, 'value="organizer" checked')


