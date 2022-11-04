import uuid


def get_session_key(request):
    """Get or create an uuid key to identify TodoList."""
    session_uuid = request.session.get("todo_uuid", str(uuid.uuid4()))
    request.session["todo_uuid"] = session_uuid
    return session_uuid
