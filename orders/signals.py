from .models import Order
from utils import send_sms
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random


# if user paid order, send it a sms
@receiver(signal=pre_save, sender=Order)
def submit_order(sender, instance, update_fields, **kwargs):

    # if not add, just update(order.paid)
    if not instance._state.adding:
        order = Order.objects.get(id=instance.id)

        # pre save
        if not order.paid and instance.ref_id is None:
            ref = str(random.randint(111111, 999999))
            send_sms(instance.address.phone_number, f'با تشکر از اعتماد شما\nسفارش شما با موفقیت ثبت شد'
                                                    f'\nکد سفارش: {str(ref)} '
                                                    f'\n\nفروشگاه لپ تاپ بانه')

            # update order
            instance.ref_id = str(ref)
            instance.save()

            # update item (product and color number)
            for item in instance.items.all():
                item.color.number -= item.quantity
                if item.color.number == 0:
                    item.color.available = False
                item.color.product.number -= item.quantity
                if item.color.product.number == 0:
                    item.color.product.available = False
                item.color.product.sell += item.quantity
                item.color.save()
                item.color.product.save()
        else:
            pass
    else:
        pass
