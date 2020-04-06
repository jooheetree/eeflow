from datetime import date, datetime, time

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from erp.services import OracleService


@api_view(['GET'])
def voucher_list(request: Request):
    start_date: list = request.query_params.get('startDate').split('-')
    end_date: list = request.query_params.get('endDate').split('-')
    start_date: str = start_date[0] + start_date[1] + start_date[2]
    end_date: str = end_date[0] + end_date[1] + end_date[2]
    search: str = request.query_params.get('search')

    columns = [
        {'ids': 'id'},
        {'RPICU': 'RPICU'},
        {'RPDGJ': 'RPDGJ'},
        {'RPALPH': 'RPALPH'},
        {'RPDL02': 'RPDL02'},
        {'RPAMT / 100': 'RPAMT'},
        {'RPRMK': 'RPRMK'},
        {'RPTORG': 'RPTORG'},
        {'RPSEQ': 'RPSEQ'},
        {'RPDCT': 'RPDCT'},
        {'RPDL02': 'RPDL02'},
        {'RPEXR1': 'RPEXR1'},
        {'RPTXA1': 'RPTXA1'},
        {'RPDOC': 'RPDOC'},
        {'RPTAX': 'RPTAX'},
        {'RPALPH': 'RPALPH'},
        {'RPSFX': 'RPSFX'},
        {'RPZ5DEBITAT': 'RPZ5DEBITAT'},
        {'RPZ5CREDITAT': 'RPZ5CREDITAT'},
        {'RPAN8': 'RPAN8'},
        {'RPTORG': 'RPTORG'},
        {'RPNAME': 'RPNAME'}
    ]
    table = 'vap_voucher'
    wheres = [f" rpdgj >= TO_DATE({start_date}, 'YYYYMMDD')",
              f" rpdgj <= TO_DATE({end_date}, 'YYYYMMDD')"]

    if search:
        wheres.append(f" RPRMK like '%{search}%'")

    service = OracleService(columns, table, wheres)
    return Response(data=service.result, status=status.HTTP_200_OK)


@api_view(['GET'])
def voucher_list_batch_number(request: Request, batch_number: int):
    # columns = [
    #     {'ids': 'id'},
    #     {'rpicu': 'batchNumber'},
    #     {'rpdgj': 'gl_ymd'},
    #     {'RPALPH': 'supplyNumber'},
    #     {'RPDL02': 'accountName'},
    #     {'RPAMT / 100': 'price'},
    #     {'RPRMK': 'bigo'},
    #     {'RPTORG': 'author'},
    # ]
    columns = [
        {'ids': 'id'},
        {'RPICU': 'RPICU'},
        {'RPDGJ': 'RPDGJ'},
        {'RPALPH': 'RPALPH'},
        {'RPDL02': 'RPDL02'},
        {'RPAMT / 100': 'RPAMT'},
        {'RPRMK': 'RPRMK'},
        {'RPTORG': 'RPTORG'},
    ]
    table = 'vap_voucher'
    wheres = [f'rpicu = {batch_number}']
    service = OracleService(columns, table, wheres)
    return Response(data=service.result, status=status.HTTP_200_OK)
