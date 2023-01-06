import os
from kavenegar import *
import random
from accounts.models import OtpCode

KAVENEGAR_API = os.environ.get('KAVENEGAR_API')


def send_sms(phone_number, message):
    try:
        api = KavenegarAPI(KAVENEGAR_API)
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
    code = random.randint(1111, 9999)
    send_sms(phone_number, f'کاربر گرامی،\nکد تائید حساب کاربری شما: {code}\nمدت اعتبار: 3 دقیقه \n\nبانه لپ تاپ شاپ')
    code_instance = OtpCode.objects.filter(phone_number=phone_number)
    if code_instance.exists():
        code_instance.delete()
    OtpCode.objects.create(phone_number=phone_number, code=code)
