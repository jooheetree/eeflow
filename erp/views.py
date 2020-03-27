import json
from requests import Request

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from erp.services import OracleService


@api_view(['GET'])
def voucher_list(request: Request):
    columns = [
        {'ids': 'id'},
        {'rpicu': 'batchNumber'},
        {'rpdgj': 'gl_ymd'},
        {'RPALPH': 'supplyNumber'},
        {'RPDL02': 'accountName'},
        {'RPAMT / 100': 'price'},
        {'RPRMK': 'bigo'},
        {'RPTORG': 'author'},
    ]
    table = 'vap_voucher'
    service = OracleService(columns, table)
    return Response(data=service.result, status=status.HTTP_200_OK)


@api_view(['GET'])
def voucher_list_batch_number(request: Request, batch_number: int):
    columns = [
        {'ids': 'id'},
        {'rpicu': 'batchNumber'},
        {'rpdgj': 'gl_ymd'},
        {'RPALPH': 'supplyNumber'},
        {'RPDL02': 'accountName'},
        {'RPAMT / 100': 'price'},
        {'RPRMK': 'bigo'},
        {'RPTORG': 'author'},
    ]
    table = 'vap_voucher'
    wheres = [f'rpicu = {batch_number}']
    service = OracleService(columns, table, wheres)
    return Response(data=service.result, status=status.HTTP_200_OK)
