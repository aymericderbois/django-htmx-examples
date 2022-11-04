from django.db import models


class TodoManager(models.Manager):
    def active(self):
        return self.filter(is_done=False)

    def completed(self):
        return self.filter(is_done=True)

class Todo(models.Model):
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    session_uuid = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
