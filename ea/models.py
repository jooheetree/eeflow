from django.contrib.auth.models import User
from django.db import models


class Push(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_data')
    endpoint = models.CharField(max_length=500)
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.user.username
