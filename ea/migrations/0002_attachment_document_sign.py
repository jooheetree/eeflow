# Generated by Django 3.0.2 on 2020-01-28 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ea', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('delete_state', models.CharField(choices=[('Y', '삭제됨'), ('N', '미삭제')], default='N', max_length=2)),
                ('doc_status', models.CharField(choices=[('0', '임시저장'), ('1', '결재대기중'), ('2', '반려'), ('3', '결재완료')], default='1', max_length=2)),
                ('sign_list', models.CharField(max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document', to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('result', models.CharField(choices=[('0', '대기중'), ('1', '다음대기'), ('2', '승인'), ('3', '반려')], default='0', max_length=2)),
                ('comment', models.TextField()),
                ('seq', models.PositiveIntegerField()),
                ('type', models.CharField(choices=[('0', '결재'), ('1', '합의'), ('2', '수신및참조')], default='0', max_length=2)),
                ('sign_date', models.DateTimeField(blank=True, null=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sign', to='ea.Document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('path', models.FileField(upload_to='attachment/')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='ea.Document')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]