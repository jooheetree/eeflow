from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from employee.models import Employee
from employee.serializers import EmployeeSerializer


@api_view(['POST'])
def get_employee(request: Request):
    if request.method == 'POST':
        token: Token = Token.objects.filter(key=request.auth).first()

        if not token:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        employee: Employee = token.user.employee
        serializer = EmployeeSerializer(employee)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
