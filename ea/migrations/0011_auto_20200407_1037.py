# Generated by Django 2.1.1 on 2020-04-07 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ea', '0010_auto_20200401_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='RPDDJ',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='RPEXR1NM',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]