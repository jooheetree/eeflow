from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Q

from ea.models import Document, Attachment, Sign, SIGN_TYPE, DefaulSignList
from employee.models import Employee
import json

from typing import List
Approvers = List[dict]


def update_batch_number(batch_number: int):
    """
    ERP Update Query 실행 : 일괄 적용
    """
    pass


@transaction.atomic
class DocumentServices:
    def __init__(self, **kwargs):
        attachments: list = kwargs.get('attachments')
        title: str = kwargs.get('title')
        batch_number: int = kwargs.get('batch_number')
        approvers: Approvers = kwargs.get('approvers')
        author: User = kwargs.get('author')

        document = self.create_document(title, author, approvers, batch_number)

        self.create_attachments(attachments, document)

        DefaulSignList.objects.filter(user=author).delete()

        for i, approver in enumerate(approvers):
            """
            approvers 순서대로 왔다고 가정
            """
            user: User = User.objects.get(username=approver.get('id'))
            self.create_sign(user, i, document)
            self.create_defaulsignlist(author, user.employee, approver.get('type'), i)

        self.send_push(document)

    def create_document(self, title: str, auhor: User, approvers: Approvers, batch_number: int) -> Document:
        sign_list: str = ''
        for approver in approvers:
            sign_list += f'{approver.get("name")} ->'

        return Document.objects.create(
            author=auhor,
            title=title,
            sign_list=sign_list,
            batch_number=batch_number
        )

    def create_attachments(self, attachments: list, document: Document) -> None:
        for attachment in attachments:
            fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/attachment/')
            filename = fs.save(attachment.name, attachment)
            is_img = False
            is_pdf = False

            if 'image' in attachment.content_type:
                is_img = True

            if 'pdf' in attachment.content_type:
                is_pdf = True

            Attachment.objects.create(
                document=document,
                title=filename,
                size=attachment.size,
                path='attachment/' + filename,
                isImg=is_img,
                isPdf=is_pdf
            )

    def create_sign(self, user: User, seq: int, document: Document) -> None:
        result = Sign.get_result_type_by_seq(seq)
        Sign.objects.create(
            user=user,
            document=document,
            seq=seq,
            result=result
        )

    def create_defaulsignlist(self, user: User, approver: Employee, type: int, order: int) -> None:
        return DefaulSignList.objects.create(
            user=user,
            approver=approver,
            type=type,
            order=order
        )

    def send_push(self, document: Document):
        sign: Sign = Sign.objects.filter(Q(document=document), Q(result=0)).first()
        pushs = sign.user.push_data.all()
        for push in pushs:
            push.send_push(f'[결재] {document.title}')
