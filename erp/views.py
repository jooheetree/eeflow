from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from ea.services import create_date_str
from employee.models import Employee
from erp.services import OracleService


@api_view(['GET'])
def voucher_list(request: Request):
    start_date: str = create_date_str(request.query_params.get('startDate'))
    end_date: str = create_date_str(request.query_params.get('endDate'))
    search: str = request.query_params.get('search')

    employees: QuerySet = Employee.objects.filter(department=request.user.employee.department)
    usernames: list = list(map(lambda employee: employee.user.username.upper(), employees))
    user_str: str = ", ".join("'{0}'".format(username) for username in usernames)

    columns = [
        {'ids': 'id'},
        {'RPCO': 'RPCO'},
        {'RPICU': 'RPICU'},
        {'RPDGJ': 'RPDGJ'},
        {'RPALPH': 'RPALPH'},
        {'RPDL02': 'RPDL02'},
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
        {'RPZ5DEBITAT / 100': 'RPZ5DEBITAT'},
        {'RPZ5CREDITAT / 100': 'RPZ5CREDITAT'},
        {'RPAN8': 'RPAN8'},
        {'RPTORG': 'RPTORG'},
        {'RPDSVJ': 'RPDSVJ'},
        {'RPEXR1NM': 'RPEXR1NM'},
        {'RPDDJ': 'RPDDJ'},
        {'RPSBLT': 'RPSBLT'},
        {'RPDL03': 'RPDL03'},
        {'RPCODE': 'RPCODE'},
        {'RPNAME': 'RPNAME'}
    ]
    table = 'vap_voucher1'
    user_where = f" RPTORG in ({user_str})"
    wheres = [f" rpdgj >= TO_DATE({start_date}, 'YYYYMMDD')",
              f" rpdgj <= TO_DATE({end_date}, 'YYYYMMDD')"]

    if not request.user.is_superuser:
        wheres.append(user_where)

    if search:
        wheres.append(f" RPRMK like '%{search}%'")

    service = OracleService()
    query = service.create_select_query(columns, table, wheres)
    result = service.get_result(query, columns)
    return Response(data=result, status=status.HTTP_200_OK)


@api_view(['GET'])
def payment_list(request: Request):
    start_date: str = create_date_str(request.query_params.get('startDate'))
    end_date: str = create_date_str(request.query_params.get('endDate'))
    search: str = request.query_params.get('search')

    employees: QuerySet = Employee.objects.filter(department=request.user.employee.department)
    usernames: list = list(map(lambda employee: employee.user.username.upper(), employees))
    user_str: str = ", ".join("'{0}'".format(username) for username in usernames)

    columns = [
        {'ids': 'id'},
        {'RPICU': 'RPICU'},
        {'RPDGJ': 'RPDGJ'},
        {'RPALPH': 'RPALPH'},
        {'RPDL02': 'RPDL02'},
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
        {'RPZ5DEBITAT / 100': 'RPZ5DEBITAT'},
        {'RPZ5CREDITAT / 100': 'RPZ5CREDITAT'},
        {'RPAN8': 'RPAN8'},
        {'RPTORG': 'RPTORG'},
        {'RPDSVJ': 'RPDSVJ'},
        {'RPEXR1NM': 'RPEXR1NM'},
        {'RPDDJ': 'RPDDJ'},
        {'RPSBLT': 'RPSBLT'},
        {'RPDL03': 'RPDL03'},
        {'RPCODE': 'RPCODE'},
        {'RPNAME': 'RPNAME'},
        # another
        {'RPDOCM': 'RPDOCM'}
    ]
    table = 'vap_payment1'
    user_where = f" RPTORG in ({user_str})"
    wheres = [f" rpdgj >= TO_DATE({start_date}, 'YYYYMMDD')",
              f" rpdgj <= TO_DATE({end_date}, 'YYYYMMDD')"]

    if not request.user.is_superuser:
        wheres.append(user_where)

    if search:
        wheres.append(f" RPRMK like '%{search}%'")

    service = OracleService()
    query = service.create_select_query(columns, table, wheres)
    result = service.get_result(query, columns)
    return Response(data=result, status=status.HTTP_200_OK)


@api_view(['GET'])
def invoice_list(request: Request):
    start_date: str = create_date_str(request.query_params.get('startDate'))
    end_date: str = create_date_str(request.query_params.get('endDate'))
    search: str = request.query_params.get('search')

    employees: QuerySet = Employee.objects.filter(department=request.user.employee.department)
    usernames: list = list(map(lambda employee: employee.user.username.upper(), employees))
    user_str: str = ", ".join("'{0}'".format(username) for username in usernames)

    columns = [
        {'ids': 'id'},
        {'RPICU': 'RPICU'},
        {'RPDGJ': 'RPDGJ'},
        {'RPALPH': 'RPALPH'},
        {'RPDL02': 'RPDL02'},
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
        {'RPZ5DEBITAT / 100': 'RPZ5DEBITAT'},
        {'RPZ5CREDITAT / 100': 'RPZ5CREDITAT'},
        {'RPAN8': 'RPAN8'},
        {'RPTORG': 'RPTORG'},
        {'RPDSVJ': 'RPDSVJ'},
        {'RPEXR1NM': 'RPEXR1NM'},
        {'RPDDJ': 'RPDDJ'},
        {'RPSBLT': 'RPSBLT'},
        {'RPDL03': 'RPDL03'},
        {'RPCODE': 'RPCODE'},
        {'RPNAME': 'RPNAME'}
    ]
    table = 'var_invoice1'
    user_where = f" RPTORG in ({user_str})"
    wheres = [f" rpdgj >= TO_DATE({start_date}, 'YYYYMMDD')",
              f" rpdgj <= TO_DATE({end_date}, 'YYYYMMDD')"]

    if not request.user.is_superuser:
        wheres.append(user_where)

    if search:
        wheres.append(f" RPRMK like '%{search}%'")

    service = OracleService()
    query = service.create_select_query(columns, table, wheres)
    result = service.get_result(query, columns)
    return Response(data=result, status=status.HTTP_200_OK)


@api_view(['GET'])
def receipt_list(request: Request):
    start_date: str = create_date_str(request.query_params.get('startDate'))
    end_date: str = create_date_str(request.query_params.get('endDate'))
    search: str = request.query_params.get('search')

    employees: QuerySet = Employee.objects.filter(department=request.user.employee.department)
    usernames: list = list(map(lambda employee: employee.user.username.upper(), employees))
    user_str: str = ", ".join("'{0}'".format(username) for username in usernames)

    columns = [
        {'ids': 'id'},
        {'RPICU': 'RPICU'},
        {'RPDGJ': 'RPDGJ'},
        {'RPALPH': 'RPALPH'},
        {'RPDL02': 'RPDL02'},
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
        {'RPZ5DEBITAT / 100': 'RPZ5DEBITAT'},
        {'RPZ5CREDITAT / 100': 'RPZ5CREDITAT'},
        {'RPAN8': 'RPAN8'},
        {'RPTORG': 'RPTORG'},
        {'RPDSVJ': 'RPDSVJ'},
        {'RPEXR1NM': 'RPEXR1NM'},
        {'RPDDJ': 'RPDDJ'},
        {'RPSBLT': 'RPSBLT'},
        {'RPDL03': 'RPDL03'},
        {'RPCODE': 'RPCODE'},
        {'RPNAME': 'RPNAME'},
        # another
        {'RPPYID': 'RPPYID'}

    ]
    table = 'var_receipt1'
    user_where = f" RPTORG in ({user_str})"
    wheres = [f" rpdgj >= TO_DATE({start_date}, 'YYYYMMDD')",
              f" rpdgj <= TO_DATE({end_date}, 'YYYYMMDD')"]

    if not request.user.is_superuser:
        wheres.append(user_where)

    if search:
        wheres.append(f" RPRMK like '%{search}%'")

    service = OracleService()
    query = service.create_select_query(columns, table, wheres)
    result = service.get_result(query, columns)
    return Response(data=result, status=status.HTTP_200_OK)


@api_view(['GET'])
def nacct_list(request: Request):
    start_date: str = create_date_str(request.query_params.get('startDate'))
    end_date: str = create_date_str(request.query_params.get('endDate'))
    search: str = request.query_params.get('search')

    employees: QuerySet = Employee.objects.filter(department=request.user.employee.department)
    usernames: list = list(map(lambda employee: employee.user.username.upper(), employees))
    user_str: str = ", ".join("'{0}'".format(username) for username in usernames)

    columns = [
        {'ids': 'id'},
        {'RPICU': 'RPICU'},
        {'RPDGJ': 'RPDGJ'},
        {'RPALPH': 'RPALPH'},
        {'RPDL02': 'RPDL02'},
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
        {'RPDSVJ': 'RPDSVJ'},
        {'RPEXR1NM': 'RPEXR1NM'},
        {'RPDDJ': 'RPDDJ'},
        {'RPSBLT': 'RPSBLT'},
        {'RPDL03': 'RPDL03'},
        {'RPCODE': 'RPCODE'},
        {'RPNAME': 'RPNAME'}
    ]
    table = 'vga_nacct1'
    user_where = f" RPTORG in ({user_str})"
    wheres = [f" rpdgj >= TO_DATE({start_date}, 'YYYYMMDD')",
              f" rpdgj <= TO_DATE({end_date}, 'YYYYMMDD')"]

    if not request.user.is_superuser:
        wheres.append(user_where)

    if search:
        wheres.append(f" RPRMK like '%{search}%'")

    service = OracleService()
    query = service.create_select_query(columns, table, wheres)
    result = service.get_result(query, columns)
    return Response(data=result, status=status.HTTP_200_OK)


