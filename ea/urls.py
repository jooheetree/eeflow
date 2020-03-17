"""eeflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from ea.views import send_push, create_document, get_defaultUsers, get_departmentUsers, allUsers, written_document, \
    create_push, delete_push

API_TITLE = 'Blog API'
API_DESCRIPTION = 'A Web API for create and edit blog'

schema_view = get_swagger_view(title=API_TITLE)


urlpatterns = [
    path('send_push/', send_push, name='send_push'),
    path('create_push/', create_push, name='create_push'),
    path('delete_push/', delete_push, name='delete_push'),
    path('create_document/', create_document, name='create_document'),
    path('written_document/<str:username>', written_document, name='written_document'),
    path('get_defaultUsers/<str:username>', get_defaultUsers, name='get_defaultUsers'),
    path('get_departmentUsers/<str:department_name>', get_departmentUsers, name='get_departmentUsers/'),
    path('get_allUsers/', allUsers, name='get_allUsers'),
]
