from django.core.management.base import BaseCommand
from products.models import Compare


class Command(BaseCommand):
    help = 'remove all Compare Objects'

    def handle(self, *args, **options):
        Compare.objects.all().delete()
