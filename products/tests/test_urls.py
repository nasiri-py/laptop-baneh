from django.test import SimpleTestCase
from django.urls import reverse, resolve
from products.views import product_list_view


class TestProductsUrl(SimpleTestCase):
    def test_product_list_view(self):
        url = reverse('product:list')
        self.assertEqual(resolve(url).func, product_list_view)