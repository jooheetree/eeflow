from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

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


def create_document(title: str, auhor: User, approvers: Approvers) -> Document:
    sign_list: str = ''
    for approver in approvers:
        sign_list += f'{approver.get("username")} ->'

    return Document.objects.create(
        author=auhor,
        title=title,
        sign_list=sign_list
    )


def create_attachments(attachments: list, document: Document) -> None:
    for attachment in attachments:
        fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/attachment/')
        filename = fs.save(attachment.name, attachment)
        Attachment.objects.create(
            document=document,
            title=filename,
            size=attachment.size,
            path=settings.MEDIA_URL + filename
        )


def sign_create(user: User, seq: int, document: Document) -> None:
    result = Sign.get_result_type_by_seq(seq)
    Sign.objects.create(
        user=user,
        document=document,
        seq=seq,
        result=result
    )


def defaulsignlist_create(user: User, approver: Employee, type: SIGN_TYPE = 0) -> None:
    return DefaulSignList.objects.create(
        user=user,
        approver=approver,
        type=type
    )
