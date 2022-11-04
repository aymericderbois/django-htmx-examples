import uuid

from django.http import HttpResponse


def get_session_key(request):
    """Get or create an uuid key to identify TodoList."""
    session_uuid = request.session.get("todo_uuid", str(uuid.uuid4()))
    request.session["todo_uuid"] = session_uuid
    return session_uuid


def htmx_redirect(url):
    return HttpResponse(
        content="",
        status=204,
        headers={"HX-Location": url},
    )
