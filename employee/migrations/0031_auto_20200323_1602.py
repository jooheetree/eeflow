# Generated by Django 2.1.1 on 2020-03-23 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0030_auto_20200323_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position', to='employee.Position'),
        ),
    ]
