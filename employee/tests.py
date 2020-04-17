from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from employee.models import Employee, POSITION_ORDER, DEPARTMENT_ORDER, Department, Position
from rest_framework.test import APIClient


class EmployeeModelTest(TestCase):
    """
    User 확장 Modal 테스트
    """

    def setUp(self) -> None:
        self.position_create()
        self.department_create()

        self.user = User.objects.create(username='seungwoo')
        self.user.set_password('seungwoo')
        self.user.first_name = '이승우'
        self.user.save()

        self.user.employee.position = Position.objects.first()
        self.user.employee.department = Department.objects.first()
        self.user.save()
        self.token: str = self.login()

        self.drf_client = APIClient()
        self.drf_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def position_create(self):
        for position in POSITION_ORDER:
            Position(**position).save()

    def department_create(self):
        for department in DEPARTMENT_ORDER:
            Department(**department).save()

    def test_employee_model(self):
        employee: Employee = Employee.objects.first()
        self.assertEqual(self.user, employee.user)
        self.assertEqual(employee.position.name, '사원')
        self.assertEqual(employee.department.name, '[사료]경영지원팀')
        # self.assertEqual(employee.get_order(), 20)

    def login(self):
        response = self.client.post('/rest-auth/login/',data={
            "username": "seungwoo",
            "password": "seungwoo",
        })
        return response.data['key']

    def test_get_employee_view(self):
        response: Response = self.drf_client.post('/employee/get_employee/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('token'), self.token)
        self.assertEqual(response.data.get('user').get('username'), 'seungwoo')
        self.assertEqual(response.data.get('user').get('first_name'), '이승우')
        self.assertEqual(response.data.get('department').get('name'), '[사료]경영지원팀')
        self.assertEqual(response.data.get('position').get('name'), '사원')

    def test_change_password_view(self):
        data = {"new_password": '1234'}
        response: Response = self.drf_client.post('/employee/change_password/', data=data)
        self.assertEqual(response.status_code, 200)
