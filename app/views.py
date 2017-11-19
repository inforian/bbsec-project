import requests, datetime
from django.http import JsonResponse
from django.conf import settings

# Create your views here.


OTP_URL = 'http://pyotp.noapp.mobi/generate-otp/hotp/'
NOTIFY_URL = 'http://notify.noapp.mobi/micro-service/notification/sms/msg91/'


def create_otp(request):
    """
    """
    phone_no = request.POST.get('phone_no')
    otp_data = {
        "count":1000
    }
    now = datetime.datetime.now()

    response = requests.post(OTP_URL, data=otp_data)
    if response.status_code == 201:
        otp = response.json().get('otp')
        body = "OTP is {0} and generated at {1}".format(otp, now)
        send_notification(body, phone_no)
        return JsonResponse(response.json())
    return JsonResponse({'detail': 'service down'}, status=400)


def notify(request):
    """
    """
    phone_no = request.POST.get('phone_no')
    body = request.POST.get('body')

    response = send_notification(body, phone_no)

    if response.status_code == 200:
        return JsonResponse({'detail': 'Notification Sent.'})
    return JsonResponse({'detail': 'service down'}, status=400)


def send_notification(body, phone_no):
    """

    """
    data = {
        "to": phone_no,
        "from_": "TESTSSS",
        "provider": "msg91",
        "body": body,
        "auth_key": getattr(settings, 'MSG_91_AUTHKEY')
    }
    return requests.post(NOTIFY_URL, data=data)