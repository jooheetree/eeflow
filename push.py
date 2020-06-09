import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eeflow.settings")
django.setup()

from ea.models import Sign
from django.contrib.auth.models import User
from django.db.models import Q, QuerySet, Count

signs: QuerySet = Sign.objects.filter(Q(is_pushed=False), Q(result=0))
push_signs = signs.values('user').annotate(document_count=Count('document'))
print(push_signs)
for sign in push_signs:
    pushs = User.objects.get(id=sign.get('user')).push_data.all()
    for push in pushs:
        push.send_push(f'[ERP 전자결재] 결재 요청')

signs: QuerySet = Sign.objects.filter(Q(is_pushed=False), Q(result=0))
for sign in signs:
    sign.is_pushed = True
    sign.save()
