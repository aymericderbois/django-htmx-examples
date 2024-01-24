import uuid
from django.http import HttpRequest

from django.utils.functional import SimpleLazyObject

from apps.todos.utils import get_session_key


class TodoSessionKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.todo_session_uuid = get_session_key(request=request)        
        return self.get_response(request)