# Generated by Django 3.0.2 on 2020-02-19 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_auto_20200219_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(max_length=50),
        ),
    ]
