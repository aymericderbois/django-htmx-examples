import uuid


def get_session_key(request):
    """Get or create an uuid key to identify TodoList."""
    session_uuid = request.session.get("todo_uuid", str(uuid.uuid4()))
    request.session["todo_uuid"] = session_uuid
    return session_uuid


class TodoSessionKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.todo_session_uuid = get_session_key(request=request)
        return self.get_response(request)
