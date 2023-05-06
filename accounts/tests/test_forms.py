from django.test import TestCase
from accounts.forms import RegisterForm
from accounts.models import User


class TestRegisteForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(phone_number='09121234567', username='testuser', password='test')

    def test_valid_data(self):
        form = RegisterForm(data={
            'phone_number': '09111111111',
            'username': 'jack',
            'password1': 'jackpass',
            'password2': 'jackpass'
        })
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_exist_phone_number(self):
        form = RegisterForm(data={
            'phone_number': '09121234567',
            'username': 'nottestuser',
            'password1': 'nottestpassword',
            'password2': 'nottestpassword'
        })
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('phone_number'))

    def test_exist_username(self):
        form = RegisterForm(data={
            'phone_number': '09000000000',
            'username': 'testuser',
            'password1': 'nottestpass',
            'password2': 'nottestpass'
        })
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('username'))

    def test_unmatched_password(self):
        form = RegisterForm(data={
            'phone_number': '09222222222',
            'username': 'testuser2',
            'password1': 'matchtestpass',
            'password2': 'unmatchtestpass'
        })