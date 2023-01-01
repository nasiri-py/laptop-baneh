from celery import shared_task
from .models import Compare


@shared_task
def remove_compare_objects():
    Compare.objects.all().delete()
