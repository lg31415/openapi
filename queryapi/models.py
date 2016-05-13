from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AreaCode(models.Model):
    area_name = models.CharField(max_length=60)
    area_code = models.CharField(max_length=60)
    area_type = models.CharField(max_length=60)

