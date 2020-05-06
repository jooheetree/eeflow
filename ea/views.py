import json
from datetime import date, datetime, time
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q, QuerySet
from django.http import HttpResponse, HttpRequest
from typing import List

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from ea.models import Push, Document, Attachment, Sign, SIGN_TYPE, DefaulSignList, DOCUMENT_TYPE
from ea.serializers import DefaultUsersSerializer, SignUsersSerializer, DocumentSerializer, PushSerializer
from ea.services import DocumentServices, Approvers, create_date, filter_document

from employee.models import Department, Employee
from erp.services import OracleService


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
    document_type: str = request.data.get('document_type')
    approvers: str = request.data.get('approvers')
    approvers: Approvers = json.loads(approvers)
    attachments_files: list = request.data.getlist('files')
    attachments_counts: list = request.data.getlist('counts')
    attachments_invoices: list = request.data.getlist('invoices')

    if Document.objects.filter(Q(batch_number=batch_number), ~Q(doc_status=2)).first():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    DocumentServices(attachments=attachments_files,
                     attachments_invoices=attachments_invoices,
                     attachments_counts=attachments_counts,
                     title=title,
                     batch_number=batch_number,
                     document_type=document_type,
                     approvers=approvers,
                     author=author)

    service = OracleService()
    service.execute_insert_query('kcfeed.eabatno',
                                 ['BATNO', 'BATDT'], [batch_number, datetime.now().strftime("%Y%m%d")])

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_defaultUsers(request: Request, username: str, document_type: str):
    doc_type = '0'
    for t in DOCUMENT_TYPE:
        if document_type == t[1]:
            doc_type = t[0]
            break

    user = User.objects.get(username=username)
    defaulSignList = DefaulSignList.objects.filter(Q(user=user), Q(document_type=doc_type))
    serializer = DefaultUsersSerializer(defaulSignList, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_departmentUsers(request: Request, department_name: str):
    department = Department.objects.get(name=department_name)
    employees = Employee.objects.filter(department=department)
    serializer = SignUsersSerializer(employees, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def allUsers(request: Request):
    employees = Employee.objects.all()
    serializer = SignUsersSerializer(employees, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def written_document(request: Request, username: str):
    start_date: date = create_date(request.query_params.get('startDate'))
    end_date: date = create_date(request.query_params.get('endDate'))
    search: str = request.query_params.get('search')
    batch_number: str = request.query_params.get('batchNumber', '')
    user: str = request.query_params.get('user', '')
    department: str = request.query_params.get('department', '')

    documents: QuerySet = Document.objects.filter(
        Q(author__username=username),
        Q(created__range=(datetime.combine(start_date, time.min),
                          datetime.combine(end_date, time.max))))

    documents = filter_document(documents, search, batch_number, user, department)

    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def approved_document(request: Request, username: str):
    start_date: date = create_date(request.query_params.get('startDate'))
    end_date: date = create_date(request.query_params.get('endDate'))
    search: str = request.query_params.get('search')
    batch_number: str = request.query_params.get('batchNumber', '')
    user: str = request.query_params.get('user', '')
    department: str = request.query_params.get('department', '')

    documents: QuerySet = Document.objects.filter(
        Q(signs__result__in=[2,3]),
        Q(signs__user__username=username),
        Q(created__range=(datetime.combine(start_date, time.min),
                          datetime.combine(end_date, time.max))))

    documents = filter_document(documents, search, batch_number, user, department)

    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def rejected_document(request: Request, username: str):
    start_date: date = create_date(request.query_params.get('startDate'))
    end_date: date = create_date(request.query_params.get('endDate'))
    search: str = request.query_params.get('search')
    batch_number: str = request.query_params.get('batchNumber', '')
    user: str = request.query_params.get('user', '')
    department: str = request.query_params.get('department', '')

    documents: QuerySet = Document.objects.filter(
        Q(signs__result=3),
        Q(author__username=username),
        Q(created__range=(datetime.combine(start_date, time.min),
                          datetime.combine(end_date, time.max))))

    documents = filter_document(documents, search, batch_number, user, department)

    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def sign_document(request: Request, username: str):
    start_date: date = create_date(request.query_params.get('startDate'))
    end_date: date = create_date(request.query_params.get('endDate'))

    search: str = request.query_params.get('search', '')
    batch_number: str = request.query_params.get('batchNumber', '')
    user: str = request.query_params.get('user', '')
    department: str = request.query_params.get('department', '')

    documents: QuerySet = Document.objects.filter(
        Q(signs__result=0),
        Q(signs__user__username=username),
        Q(created__range=(datetime.combine(start_date, time.min),
                          datetime.combine(end_date, time.max))))

    if search:
        documents = documents.filter(title__contains=search)

    serializer = DocumentSerializer(documents, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def do_sign(request: Request):
    document_id: int = request.data.get('document_id')
    username: str = request.data.get('username')
    opinion: str = request.data.get('opinion')
    sign_type: str = request.data.get('sign_type')

    document: Document = Document.objects.get(id=document_id)
    sign: Sign = document.signs.get(user__username=username)
    sign.approve_sign(opinion) if sign_type == '승인' else sign.deny_sign(opinion)

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.atomic
def do_sign_all(request: Request):
    document_ids: list = request.data.get('document_ids')

    for document_id in document_ids:
        document: Document = Document.objects.get(id=document_id)
        sign: Sign = document.signs.first().get_stand_by_sign()
        sign.approve_sign('')

    return Response(status=status.HTTP_200_OK)
