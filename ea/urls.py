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

from ea.views import send_push, create_document

API_TITLE = 'Blog API'
API_DESCRIPTION = 'A Web API for create and edit blog'

schema_view = get_swagger_view(title=API_TITLE)


urlpatterns = [
    path('push/', send_push, name='send_push'),
    path('create_document/', create_document, name='create_document'),
]
