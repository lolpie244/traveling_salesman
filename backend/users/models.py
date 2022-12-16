from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from .choices import MethodsEnum


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history")
    path = ArrayField(base_field=models.JSONField())
    length = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

