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
    {'name': '조장', 'order': 120},
]

DEPARTMENT_ORDER = [
    {'name': '[사료]경영지원팀', 'order': 310},
    {'name': '[사료]전산팀', 'order': 320},
    {'name': '[사료]구매팀', 'order': 330},
    {'name': '[사료]생산팀', 'order': 340},
    {'name': '[사료]영업팀', 'order': 350},
    {'name': '[사료]연구개발팀', 'order': 360},
    {'name': '[사료]임원', 'order': 370},

    {'name': '[식품]관리팀', 'order': 210},
    {'name': '[식품]생산팀', 'order': 220},
    {'name': '[식품]영업팀', 'order': 230},
    {'name': '[식품]기획팀', 'order': 240},
    {'name': '[식품]임원', 'order': 250},
]


class Department(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


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

    def __str__(self):
        return f'{self.department} {self.user.first_name} {self.position}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.employee.save()
