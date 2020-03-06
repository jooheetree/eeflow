from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpRequest, JsonResponse
from typing import List

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.views import APIView

from ea.models import Push, Document, Attachment, Sign, SIGN_TYPE, DefaulSignList
from ea.serializers import DefaultUsersSerializer, SignUsersSerializer, DocumentSerializer
from ea.services import DocumentServices, Approvers
import json

from employee.models import Department, Employee


def send_push(request: HttpRequest):
    if request.method == 'POST':
        pushes: List[Push] = request.user.push_data.all()
        for push in pushes:
            push.send_push('이승우짱!!!')
        return HttpResponse('<H1>HI</H1>')


@api_view(['POST'])
def create_document(request: Request):
    author: str = request.data.get('author')
    author: User = User.objects.get(username=author)
    title: str = request.data.get('title')
    batch_number: int = request.data.get('batch_number')
    approvers: str = request.data.get('approvers')
    approvers: Approvers = json.loads(approvers)
    attachments: list = request.data.getlist('attachments')

    DocumentServices(attachments=attachments,
                     title=title,
                     batch_number=batch_number,
                     approvers=approvers,
                     author=author)

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_defaultUsers(request: Request, username: str):
    user = User.objects.get(username=username)
    defaulSignList = DefaulSignList.objects.filter(user=user)
    serializer = DefaultUsersSerializer(defaulSignList, many=True)
    return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def get_departmentUsers(request: Request, department_name: str):
    department = Department.objects.get(name=department_name)
    employees = Employee.objects.filter(department=department)
    serializer = SignUsersSerializer(employees, many=True)
    return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def allUsers(request: Request):
    pass


@api_view(['GET'])
def written_document(request: Request, username: str):
    documents = Document.objects.filter(author__username=username)
    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
