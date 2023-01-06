from django.core.management.base import BaseCommand
from orders.models import Order


class Command(BaseCommand):
    help = 'remove all unpaid Orders'

    def handle(self, *args, **options):
        Order.objects.filter(paid=False).delete()
