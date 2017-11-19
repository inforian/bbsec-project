"""

"""

from django.conf.urls import url, include
from app.views import create_otp, notify

urlpatterns = [
    url(r'^create-otp/$', create_otp),
    url(r'^notify/$', notify),

]