from django.db import models


class TodoQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_done=False)

    def completed(self):
        return self.filter(is_done=True)

    def from_session(self, session_uuid):
        return self.filter(session_uuid=session_uuid)


class TodoManager(models.Manager.from_queryset(TodoQuerySet)):
    def toggle_all(self, session_uuid):
        qs = self.model.objects.from_session(session_uuid)
        if qs.filter(is_done=False).count() == 0:
            qs.update(is_done=False)
        else:
            qs.update(is_done=True)


class Todo(models.Model):
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    session_uuid = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = TodoManager()
