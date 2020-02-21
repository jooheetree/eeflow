from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum

POSITION_ORDER = [
    {'name': '사원', 'order': 10},
    {'name': '주임', 'order': 20},
    {'name': '대리', 'order': 30},
    {'name': '과장', 'order': 40},
    {'name': '차장', 'order': 50},
    {'name': '이사보', 'order': 60},
    {'name': '상무이사', 'order': 70},
    {'name': '전무이사', 'order': 80},
    {'name': '부사장', 'order': 90},
    {'name': '사장', 'order': 100},
    {'name': '회장', 'order': 110},
]

DEPARTMENT_ORDER = [
    {'name': '[사료]경영지원팀', 'order': 10},
    {'name': '[사료]전산팀', 'order': 20},
    {'name': '[사료]구매팀', 'order': 30},
    {'name': '[사료]생산팀', 'order': 40},
    {'name': '[사료]영업팀', 'order': 50},
    {'name': '[식품]영업팀', 'order': 60},
]


class Department(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()


class Position(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='position',
                                 blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department',
                                   blank=True, null=True)
    avatar = models.ImageField(blank=True, upload_to='avatar/')

    def get_order(self):
        pass
        # return POSITION_ORDER[self.position]


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.employee.save()
