from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from pywebpush import webpush, WebPushException
from requests import Request
from typing import List
from ea.models import Push
from employee.models import Employee


def send_push(request: HttpRequest):
    if request.method == 'POST':
        pushes: List[Push] = request.user.push_data.all()
        for push in pushes:
            push.send_push('이승우짱!!!')
        return HttpResponse('<H1>HI</H1>')


def create_document(request: HttpRequest):
    if request.method == 'POST':
        username: str = request.POST.get('username', '')
        title: str = request.POST.get('title', '')
        files: list = request.POST.get('files', [])

        # file_title = title,
        # file_size = size,
        # file_path = settings.MEDIA_URL + path

        User.objects.get(username=username)

        # self.title = '업무종결보고서'
        # self.sign_list = '이철용->윤주영'
        # return Document.objects.create(
        #     author=self.user,
        #     group=self.group,
        #     title=self.title,
        #     sign_list=self.sign_list
        # )
        # token: Token = Token.objects.filter(key=request.auth).first()
        #
        # if not token:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        #
        # employee: Employee = token.user.employee
        # serializer = EmployeeSerializer(employee)
        return HttpResponse(status=201)
