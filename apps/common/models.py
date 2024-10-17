from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created = models.DateTimeField(db_index=True, default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
