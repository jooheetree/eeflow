# Generated by Django 3.0.2 on 2020-01-30 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ea', '0004_sign_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sign',
            name='result',
            field=models.CharField(choices=[('0', '대기중'), ('1', '다음대기'), ('2', '승인'), ('3', '반려')], default='1', max_length=2),
        ),
    ]
