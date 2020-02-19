from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from pywebpush import webpush, WebPushException
from requests import Request
from typing import List
from ea.models import Push


def send_push(request: HttpRequest):
    if request.method == 'POST':
        pushes: List[Push] = request.user.push_data.all()
        for push in pushes:
            push.send_push('이승우짱!!!')
        return HttpResponse('<H1>HI</H1>')
