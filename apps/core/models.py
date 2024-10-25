from django.db import models
from .mangers import LogicManager


# Create your models here.

class DeleteLogic(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = LogicManager()

    class Meta:
        abstract = True


class DailyVisit(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)
    url = models.URLField(max_length=250,null=True, blank=True)
    user = models.CharField(max_length=250, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)