from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=128)
    parent = models.ForeignKey('self')

