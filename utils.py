# from kavenegar import *
#
#
# def send_sms(phone_number, message):
#     try:
#         api = KavenegarAPI('')
#         params = {
#             'sender': '',
#             'receptor': str(phone_number),
#             'message': message
#         }
#         response = api.sms_send(params)
#         print(response)
#     except APIException as e:
#         print(e)
#     except HTTPException as e:
#         print(e)
#     pass
