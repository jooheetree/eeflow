# Generated by Django 2.1.1 on 2020-06-01 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ea', '0022_auto_20200506_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='sign',
            name='is_pushed',
            field=models.BooleanField(default=False),
        ),
    ]