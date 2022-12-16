from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings


Workers = settings.REDIS_CLIENT


class WorkersSettings(models.Model):
    class Meta:
        verbose_name = "WorkersSettings"
        verbose_name_plural = "WorkersSettings"

    clients_count = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    min_servers_count = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    max_servers_count = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    prefered_load = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=80)
    worker_timeout = models.IntegerField(validators=[MinValueValidator(0)], default=10)

