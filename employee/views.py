from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from employee.models import Employee
from employee.serializers import EmployeeWithTokenSerializer


@api_view(['POST'])
def get_employee(request: Request):
    token: Token = Token.objects.filter(key=request.auth).first()

    if not token:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    employee: Employee = token.user.employee
    serializer = EmployeeWithTokenSerializer(employee)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def change_password(request: Request):
    new_password = request.data.get('new_password')
    if not new_password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    request.user.set_password(new_password)
    request.user.save()
    return Response(status=status.HTTP_200_OK)
