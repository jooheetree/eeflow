from django.contrib.auth.models import User, Group
from django.db import models
from typing import Union

from pywebpush import webpush, WebPushException

from django.conf import settings

DELETE_STATE_CHOICES = (
    ('Y', '삭제됨'),
    ('N', '미삭제'),
)

DOC_STATUS = (
    ('0', '임시저장'),
    ('1', '결재대기중'),
    ('2', '반려'),
    ('3', '결재완료'),
)

SIGN_RESULT = (
    ('0', '대기중'),
    ('1', '다음대기'),
    ('2', '승인'),
    ('3', '반려'),
)

SIGN_TYPE = (
    ('0', '결재'),
    ('1', '합의'),
    ('2', '수신및참조'),
)


class TimeStampedModel(models.Model):
    """
        created , modified field 제공해주는 abstract base class model
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Push(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_data')
    endpoint = models.CharField(max_length=500)
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)

    objects = models.Manager()

    def get_subscription_info(self) -> dict:
        return {"endpoint": self.endpoint, "keys": {"p256dh": self.p256dh, "auth": self.auth}}

    def send_push(self, content):
        try:
            webpush(
                subscription_info=self.get_subscription_info(),
                data=content,
                vapid_private_key=settings.PUSH_PRIVATE_KEY,
                vapid_claims={
                    "sub": "mailto:leemoney93@naver.com",
                }
            )
        except WebPushException as ex:
            print("I'm sorry, Dave, but I can't do that: {}", repr(ex))

    def __str__(self):
        return self.user.username


class Document(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='document')
    title = models.CharField(max_length=255)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )
    doc_status = models.CharField(
        max_length=2,
        choices=DOC_STATUS,
        default='1',
    )
    sign_list = models.CharField(max_length=255)

    def finish_deny(self, push_content) -> None:
        self.doc_status = '2'

        for push in self.author.push_data.all():
            push.send_push(push_content)

    def finish_approve(self) -> None:
        self.doc_status = '3'


class Attachment(TimeStampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='attachment')
    title = models.CharField(max_length=255)
    size = models.PositiveIntegerField()
    path = models.FileField(upload_to='attachment/')
    isImg = models.BooleanField(default=True)


class Sign(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sign')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='sign')
    result = models.CharField(
        max_length=2,
        choices=SIGN_RESULT,
        default='1',
    )
    comment = models.TextField(null=True, blank=True)
    seq = models.PositiveIntegerField()
    type = models.CharField(
        max_length=2,
        choices=SIGN_TYPE,
        default='0',
    )
    sign_date = models.DateTimeField(null=True, blank=True)

    def get_next_sign(self) -> Union['Sign', None]:
        return self.__class__.objects.filter(document=self.document, seq=self.seq+1).first()

    def get_stand_by_sign(self):
        return self.__class__.objects.filter(document=self.document, result='0').first()

    @staticmethod
    def get_result_type_by_seq(seq: int) -> SIGN_RESULT:
        if seq == 1:
            return '0'

        return '1'

    def stand_by(self) -> None:
        self.result = '0'

    def approve(self) -> None:
        self.result = '2'

    def deny(self) -> None:
        self.result = '3'

    def notify_next_user(self, content):
        self.stand_by()
        for push in self.user.push_data.all():
            push.send_push(content)

