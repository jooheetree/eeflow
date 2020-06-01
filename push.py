import os
import django
from django.db.models import Q, QuerySet

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eeflow.settings")
django.setup()

from ea.models import Sign

signs: QuerySet = Sign.objects.filter(Q(is_pushed=False), Q(result=0))
for sign in signs:
    pushs = sign.user.push_data.all()
    for push in pushs:
        push.send_push(f'[결재] {sign.document.title}')
