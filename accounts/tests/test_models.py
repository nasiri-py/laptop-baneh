from django.test import TestCase
from accounts.models import User, OtpCode
from model_bakery import baker


class TestUserModel(TestCase):
    def setUp(self):
        self.user = baker.make(User, username='usertest', phone_number='09999999999')
    def test_model_str(self):
        self.assertEqual(str(self.user), 'usertest - 09999999999')


class TestOtpCodeModel(TestCase):
    def setUp(self):
        self.otp = baker.make(OtpCode, phone_number='09999999999', code='1234')
    def test_model_str(self):
        self.assertEqual(str(self.otp), '09999999999 - 1234')
