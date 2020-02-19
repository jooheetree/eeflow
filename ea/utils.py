import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "eeflow.settings"
django.setup()
from ea.models import Push
from pywebpush import webpush, WebPushException
from django.conf import settings
from django.contrib.auth.models import User



# try:
#     webpush(
#         subscription_info=subscription_info,
#         data="Mary had a little lamb, with a nice mint jelly",
#         vapid_private_key=settings.PUSH_PRIVATE_KEY,
#         vapid_claims={
#             "sub": "mailto:leemoney93@naver.com",
#         }
#     )
# except WebPushException as ex:
#     print("I'm sorry, Dave, but I can't do that: {}", repr(ex))
#     # Mozilla returns additional information in the body of the response.
#     if ex.response and ex.response.json():
#         extra = ex.response.json()
#         print("Remote service replied with a {}:{}, {}",
#               extra.code,
#               extra.errno,
#               extra.message
#               )
