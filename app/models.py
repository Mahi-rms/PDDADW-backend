from django.db import models
import uuid
# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, db_column="id",default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

class TokenBlackList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token=models.CharField(max_length=200, blank=True, null=True)
    expiry=models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

class PatientDetails(models.Model):
    id = models.UUIDField(primary_key=True, db_column="id",default=uuid.uuid4, editable=False)
    full_name = models.CharField(blank=True, null=True, max_length=200)
    age=models.IntegerField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=30)
    xray_hash = models.CharField(blank=True, null=True, max_length=200)
    pneumonia_result=models.CharField(blank=True, null=True, max_length=80)
    tuberculosis_result=models.CharField(blank=True, null=True, max_length=80)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)