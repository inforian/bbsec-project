from django.shortcuts import render
import requests, datetime
from django.http import JsonResponse
# Create your views here.


OTP_URL = 'http://localhost:8017/generate-otp/hotp/'


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
    url = 'http://local.veris.in:8001/micro-service/notification/sms/msg91/'

    data = {
        "to": phone_no,
        "from_": "TESTSSS",
        "provider": "msg91",
        "body": body,
        "auth_key": "176999AezfzhYs3c59f19ef6"
    }
    return requests.post(url, data=data)