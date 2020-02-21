from django.urls import path, include
from employee.views import get_employee


urlpatterns = [
    path('get_employee/', get_employee, name='get_employee'),
]
