from django.test import SimpleTestCase
from django.urls import reverse, resolve
from orders.views import order_detail_view


class TestOrderUrl(SimpleTestCase):
    def test_order_detail_view(self):
        url = reverse('orders:order-detail')
        self.assertEqual(resolve(url).func, order_detail_view)