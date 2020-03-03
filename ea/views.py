from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from pywebpush import webpush, WebPushException
from requests import Request
from typing import List

from rest_framework import status
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from ea.models import Push, Document, Attachment, Sign, SIGN_TYPE, DefaulSignList
from ea.services import create_document, create_attachments, sign_create, defaulsignlist_create, Approvers
from employee.models import Employee
import json


def send_push(request: HttpRequest):
    if request.method == 'POST':
        pushes: List[Push] = request.user.push_data.all()
        for push in pushes:
            push.send_push('이승우짱!!!')
        return HttpResponse('<H1>HI</H1>')


class CreateDocument(APIView):

    def post(self, request: Request):
        attachments: list = request.data.getlist('attachments')
        title: str = request.data.get('title')
        batch_number: int = request.data.get('batch_number')
        approvers: str = request.data.get('approvers')
        approvers: Approvers = json.loads(approvers)
        author: str = request.data.get('author')
        author: User = User.objects.get(username=author)

        self.transaction_create_document(attachments=attachments,
                                         title=title,
                                         batch_number=batch_number,
                                         approvers=approvers,
                                         author=author)

        return Response(status=status.HTTP_201_CREATED)

    @transaction.atomic
    def transaction_create_document(self, **kwargs):
        attachments: list = kwargs.get('attachments')
        title: str = kwargs.get('title')
        batch_number: int = kwargs.get('batch_number')
        approvers: Approvers = kwargs.get('approvers')
        author: User = kwargs.get('author')

        document = create_document(title, author, approvers)

        create_attachments(attachments, document)

        for i, approver in enumerate(approvers):
            user: User = User.objects.get(username=approver.get('username'))
            sign_create(user, i, document)
            defaulsignlist_create(author, user.employee, )
