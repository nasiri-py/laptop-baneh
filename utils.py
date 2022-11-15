from kavenegar import *
import random
from accounts.models import OtpCode


def send_sms(phone_number, message):
    try:
        api = KavenegarAPI('')
        params = {
            'sender': '',
            'receptor': str(phone_number),
            'message': message
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def send_otp_code(phone_number):
    code = random.randint(1000, 9999)
    send_sms(phone_number, f'Your verification code is {code}')
    code_instance = OtpCode.objects.filter(phone_number=phone_number)
    if code_instance.exists():
        code_instance.delete()
    OtpCode.objects.create(phone_number=phone_number, code=code)
