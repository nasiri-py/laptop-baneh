from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'remove all expired Otp Codes'

    def handle(self, *args, **options):
        expired_time = datetime.now() - timedelta(minutes=3)
        OtpCode.objects.filter(created__lt=expired_time).delete()
