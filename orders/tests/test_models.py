from django.test import TestCase
from orders.models import Order
from accounts.models import User
from model_bakery import baker


class TestOrderModel(TestCase):
    def setUp(self):
        user = baker.make(User, username='usertest', phone_number='09999999999')
        self.order = baker.make(Order, user=user)

    def test_model_str(self):
        self.assertEqual(str(self.order), 'usertest - 09999999999 - False')
