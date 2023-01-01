from celery import shared_task
from .models import Order


@shared_task
def remove_unpaid_orders():
    Order.objects.filter(paid=False).delete()
