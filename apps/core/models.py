from django.db import models
from .mangers import LogicManager


# Create your models here.

class DeleteLogic(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = LogicManager()

    class Meta:
        abstract = True
