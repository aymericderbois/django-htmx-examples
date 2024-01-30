from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
