from django.urls import path
from employee.views import get_employee, change_password

urlpatterns = [
    path('get_employee/', get_employee, name='get_employee'),
    path('change_password/', change_password, name='change_password'),
]
