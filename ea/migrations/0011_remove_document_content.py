# Generated by Django 3.0.2 on 2020-02-28 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ea', '0010_auto_20200228_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='content',
        ),
    ]