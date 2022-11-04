from todomvc.core.models import Todo
from todomvc.core.utils import get_session_key


def get_todo_queryset_from_session(request):
    return Todo.objects.from_session(get_session_key(request))
