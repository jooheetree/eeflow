import json

from django.http import HttpResponse
from django.shortcuts import render
from requests import Request

from erp.services import OracleService


def voucher_list(request: Request):
    columns = [
        {'ROWNUM': 'id'},
        {'rpicu': 'batchNumber'},
        {'rpdgj': 'gl_ymd'},
        {'RPALPH': 'supplyNumber'},
        {'RPDL02': 'accountName'},
        {'RPAMT / 100': 'price'},
        {'RPRMK': 'bigo'},
        {'RPTORG': 'author'},
    ]
    table = 'vap_voucher'
    # query = "select " \
    #         "rpicu as batchNumber, " \
    #         "f_get_jd(rpdgj) as gl_ymd," \
    #         "RPALPH as supplyNumber, " \
    #         "RPDL02 as accountName, " \
    #         "RPZ5CREDITAT as price, " \
    #         "RPRMK as bigo " \
    #         "from proddta.EA_AP_Voucher"
    service = OracleService(columns, table)
    return HttpResponse(content=json.dumps(service.result), content_type='application/json')
    # return HttpResponse('<H1>HI</H1>')
