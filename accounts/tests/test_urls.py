from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import RegisterView


class TestAccountsUrl(SimpleTestCase):
    def test_register_view(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)