# Generated by Django 4.2 on 2023-04-10 16:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDetails',
            fields=[
                ('id', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('age', models.IntegerField(max_length=3)),
                ('gender', models.CharField(blank=True, max_length=30, null=True)),
                ('xray_hash', models.CharField(blank=True, max_length=200, null=True)),
                ('pneumonia_result', models.CharField(blank=True, max_length=80, null=True)),
                ('tuberculosis_result', models.CharField(blank=True, max_length=80, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TokenBlackList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, max_length=200, null=True)),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
