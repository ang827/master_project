from django.db import models

from django.db import models

class Report(models.Model):  #建立report的数据表
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

