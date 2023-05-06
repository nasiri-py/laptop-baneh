from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from accounts.forms import RegisterForm, ProfileForm


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_GET(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.failUnless(response.context['form'], RegisterForm)

    def test_register_POST_valid(self):
        response = self.client.post(reverse('accounts:register'),
                                            data={'phone_number': '09111111111', 'username': 'test',
                                                  'password1': 'testpassword', 'password2': 'testpassword',
                                                  'from_client': 'True'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:verify'))

    def test_register_POST_invalid(self):
        response = self.client.post(reverse('accounts:register'),
                                            data={'phone_number': 'invalid', 'username': 'test',
                                                  'password1': 'testpassword', 'password2': 'testpassword',
                                                  'from_client': 'True'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(form=response.context['form'], field='phone_number',
                             errors=['فرمت شماره موبایل صحیح نمیباشد.'])


class TestProfileView(TestCase):
    def setUp(self):
        User.objects.create_user(phone_number='09121234567', username='testuser', password='test')
        self.client = Client()
        self.client.login(username='testuser', password='test')

    def test_profile_GET(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')
        self.failUnless(response.context['form'], ProfileForm)