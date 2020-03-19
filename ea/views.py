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
from ea.serializers import DefaultUsersSerializer, SignUsersSerializer, DocumentSerializer, PushSerializer
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
def create_push(request: Request):
    push_info: dict = request.data.get('pushInfo')
    data = {'user': request.user.id,
            'endpoint': push_info.get('endpoint'),
            'p256dh': push_info.get('keys').get('p256dh'),
            'auth': push_info.get('keys').get('auth')}

    if Push.objects.filter(endpoint=push_info.get('endpoint')):
        return Response(status=status.HTTP_200_OK)

    serializer = PushSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_push(request: Request):
    endpoint: str = request.data.get('endpoint')
    push: Push = Push.objects.get(endpoint=endpoint)
    push.delete()
    # push_info: dict = request.data.get('pushInfo')
    # data = {'user': request.user.id,
    #         'endpoint': push_info.get('endpoint'),
    #         'p256dh': push_info.get('keys').get('p256dh'),
    #         'auth': push_info.get('keys').get('auth')}
    #
    # if Push.objects.filter(endpoint=push_info.get('endpoint')):
    #     return Response(status=status.HTTP_200_OK)
    #
    # serializer = PushSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_200_OK)


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
    employees = Employee.objects.all()
    serializer = SignUsersSerializer(employees, many=True)
    return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def written_document(request: Request, username: str):
    documents = Document.objects.filter(author__username=username)
    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def approved_document(request: Request, username: str):
    documents = Document.objects.filter(Q(signs__user__username=username), Q(signs__result=2))
    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def rejected_document(request: Request, username: str):
    documents = Document.objects.filter(Q(signs__user__username=username), Q(signs__result=3))
    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def sign_document(request: Request, username: str):
    documents = Document.objects.filter(Q(signs__result=0), Q(signs__user__username=username))
    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def do_sign(request: Request):
    document_id: int = request.data.get('document_id')
    username: str = request.data.get('username')
    opinion: str = request.data.get('opinion')
    sign_type: str = request.data.get('sign_type')

    document: Document = Document.objects.get(id=document_id)
    sign = document.signs.get(user__username=username)
    sign.approve_sign(opinion) if sign_type == '승인' else sign.deny_sign(opinion)

    # documents = Document.objects.filter(Q(signs__result=0), Q(signs__user__username=username))
    # serializer = DocumentSerializer(documents, many=True)
    return Response(status=status.HTTP_200_OK)

