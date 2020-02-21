from django.contrib.auth.models import User
from rest_framework import serializers
from employee.models import Employee, Department, Position


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'first_name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['user', 'department', 'position', 'avatar', 'token']

    def get_token(self, employee: Employee):
        return employee.user.auth_token.key
