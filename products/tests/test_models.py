from django.test import TestCase
from products.models import Product
from model_bakery import baker


class TestProductModel(TestCase):
    def setUp(self):
        self.product = baker.make(Product, title='producttest')

    def test_model_str(self):
        self.assertEqual(str(self.product), 'producttest')
