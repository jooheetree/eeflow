from django.contrib.auth.models import User, Group
from django.db import models
from typing import Union

from pywebpush import webpush, WebPushException

from django.conf import settings
from django.utils import timezone

from employee.models import Employee, Department
from erp.services import OracleService

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
    batch_number = models.PositiveIntegerField()

    def finish_deny(self, push_content: str) -> None:
        self.doc_status = '2'
        self.save()

        for push in self.author.push_data.all():
            push.send_push(push_content)

    def finish_approve(self, push_content: str) -> None:
        self.doc_status = '3'
        self.save()

        for push in self.author.push_data.all():
            push.send_push(push_content)

    def __str__(self):
        return f'{self.title}({self.author.first_name})'


class Invoice(TimeStampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='invoices')
    IDS = models.CharField(max_length=100)
    RPSEQ = models.CharField(max_length=10)
    RPJELN = models.CharField(max_length=10)
    RPDOC = models.CharField(max_length=50)
    RPICU = models.CharField(max_length=30)
    RPICUT = models.CharField(max_length=10)
    RPDCT = models.CharField(max_length=10)
    RPCRCD = models.CharField(max_length=10)
    RPTAX = models.CharField(max_length=50, null=True, blank=True)
    RPALPH = models.CharField(max_length=255, null=True, blank=True)
    RPDGJ = models.CharField(max_length=10)
    RPDSVJ = models.CharField(max_length=10)
    RPEXR1 = models.CharField(max_length=10, null=True, blank=True)
    RPTXA1 = models.CharField(max_length=10, null=True, blank=True)
    RPPO = models.CharField(max_length=50, null=True, blank=True)
    RPCRR = models.CharField(max_length=50, null=True, blank=True)
    RPMCU = models.CharField(max_length=20)
    RPOBJ = models.CharField(max_length=20)
    RPSUB = models.CharField(max_length=20)
    RPASID = models.CharField(max_length=255, null=True, blank=True)
    RPDC = models.CharField(max_length=50, null=True, blank=True)
    RPZ5DEBITAT = models.IntegerField()
    RPZ5CREDITAT = models.IntegerField()
    RPAMT = models.IntegerField()
    RPZ5FDEDIT = models.IntegerField()
    RPZ5FCREDIT = models.IntegerField()
    RPDL02 = models.CharField(max_length=255)
    RPSFX = models.CharField(max_length=10)
    RPRMK = models.CharField(max_length=500)
    RPPDCT = models.CharField(max_length=20, null=True, blank=True)
    RPSBLT = models.CharField(max_length=255, null=True, blank=True)
    RPADDN = models.CharField(max_length=255, null=True, blank=True)
    RPPYE = models.CharField(max_length=20)
    RPDL03 = models.CharField(max_length=255)
    RPOST = models.CharField(max_length=255, null=True, blank=True)
    RPAN8 = models.CharField(max_length=20, null=True, blank=True)
    RPGLC = models.CharField(max_length=10, null=True, blank=True)
    RPTORG = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.RPDGJ}({self.RPRMK})'

    QUERY_COLUMS = [
        {'IDS': 'IDS'},
        {'RPSEQ': 'RPSEQ'},
        {'RPJELN': 'RPJELN'},
        {'RPDOC': 'RPDOC'},
        {'RPICU': 'RPICU'},
        {'RPICUT': 'RPICUT'},
        {'RPDCT': 'RPDCT'},
        {'RPCRCD': 'RPCRCD'},
        {'RPTAX': 'RPTAX'},
        {'RPALPH': 'RPALPH'},
        {'RPDGJ': 'RPDGJ'},
        {'RPDSVJ': 'RPDSVJ'},
        {'RPEXR1': 'RPEXR1'},
        {'RPTXA1': 'RPTXA1'},
        {'RPPO': 'RPPO'},
        {'RPCRR': 'RPCRR'},
        {'RPMCU': 'RPMCU'},
        {'RPOBJ': 'RPOBJ'},
        {'RPSUB': 'RPSUB'},
        {'RPASID': 'RPASID'},
        {'RPZ5DEBITAT': 'RPZ5DEBITAT'},
        {'RPZ5CREDITAT': 'RPZ5CREDITAT'},
        {'RPAMT': 'RPAMT'},
        {'RPZ5FDEDIT': 'RPZ5FDEDIT'},
        {'RPZ5FCREDIT': 'RPZ5FCREDIT'},
        {'RPDL02': 'RPDL02'},
        {'RPSFX': 'RPSFX'},
        {'RPRMK': 'RPRMK'},
        {'RPPDCT': 'RPPDCT'},
        {'RPSBLT': 'RPSBLT'},
        {'RPADDN': 'RPADDN'},
        {'RPPYE': 'RPPYE'},
        {'RPDL03': 'RPDL03'},
        {'RPOST': 'RPOST'},
        {'RPAN8': 'RPAN8'},
        {'RPGLC': 'RPGLC'},
        {'RPTORG': 'RPTORG'},
    ]

    @staticmethod
    def query_invoices(wheres: list):
        columns = Invoice.QUERY_COLUMS
        table = 'vap_voucher'
        wheres = wheres
        service = OracleService(columns, table, wheres)
        return service.result


class Attachment(TimeStampedModel):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='attachments')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='attachments')
    title = models.CharField(max_length=255)
    size = models.PositiveIntegerField()
    path = models.FileField(upload_to='attachment/')
    isImg = models.BooleanField(default=False)
    isPdf = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}({self.size}KB)'


class Sign(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sign')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='signs')
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
        return self.__class__.objects.filter(document=self.document, seq=self.seq + 1).first()

    def get_stand_by_sign(self):
        return self.__class__.objects.filter(document=self.document, result='0').first()

    @staticmethod
    def get_result_type_by_seq(seq: int) -> SIGN_RESULT:
        if seq == 0:
            return '0'

        return '1'

    def stand_by(self) -> None:
        self.result = '0'

    def approve(self) -> None:
        self.result = '2'

    def deny(self) -> None:
        self.result = '3'

    def notify_next_user(self, content: str) -> None:
        self.stand_by()
        self.save()
        for push in self.user.push_data.all():
            push.send_push(content)

    def approve_sign(self, comment: str) -> None:
        self.approve()
        self.comment = comment
        self.sign_date = timezone.now()
        self.save()

        next_sign = self.get_next_sign()

        if next_sign:
            next_sign.notify_next_user(f'[결재요청] {self.document.title}')
        else:
            self.document.finish_approve(f'[결재완료] {self.document.title}')

    def deny_sign(self, comment: str) -> None:
        self.deny()
        self.comment = comment
        self.sign_date = timezone.now()
        self.save()
        self.document.finish_deny(f'[반려] {self.document.title}')

    def __str__(self):
        return f'{self.document.title}({self.user.first_name}) {self.seq}번째'


class DefaulSignList(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='default_sign_list')
    approver = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='+')
    type = models.CharField(
        max_length=2,
        choices=SIGN_TYPE,
        default='0',
    )
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.user.first_name}_{self.approver.user.first_name}/{self.order}번째'
