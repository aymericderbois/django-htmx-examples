from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .shortcuts import get_todo_queryset_from_session
from ..core.form import TodoForm
from ..core.models import Todo
from ..core.utils import htmx_redirect, get_session_key


@require_http_methods(["GET"])
def todo_list(request, filter_by="all"):
    qs = get_todo_queryset_from_session(request).order_by("-created_at")

    todos = qs.all()
    if filter_by == "active":
        todos = todos.active()
    elif filter_by == "completed":
        todos = todos.completed()

    number_todo_active = qs.active().count()
    number_todo_completed = qs.completed().count()
    form = TodoForm()
    return render(request, "fbv_hx_location/todo_list.html", context=locals())


@require_http_methods(["GET"])
def todo_list_active(request):
    return todo_list(request, filter_by="active")


@require_http_methods(["GET"])
def todo_list_completed(request):
    return todo_list(request, filter_by="completed")


@require_http_methods(["POST"])
def todo_toggle(request, pk: int):
    todo = get_todo_queryset_from_session(request).get(pk=pk)
    todo.is_done = not todo.is_done
    todo.save()
    return htmx_redirect(request.htmx.current_url)


@require_http_methods(["POST"])
def todo_toggle_all(request):
    Todo.objects.toggle_all(get_session_key(request))
    return htmx_redirect(request.htmx.current_url)


@require_http_methods(["GET"])
def todo_partial_item(request, pk: int):
    todo = Todo.objects.from_session(get_session_key(request)).get(pk=pk)
    return render(request, "fbv_hx_location/todo_item.html", context=locals())


@require_http_methods(["POST"])
def todo_create(request):
    form = TodoForm(request.POST)
    if form.is_valid():
        form.instance.session_uuid = get_session_key(request)
        form.save()
    return htmx_redirect(request.htmx.current_url)


@require_http_methods(["GET", "POST"])
def todo_edit(request, pk: int):
    todo = Todo.objects.from_session(get_session_key(request)).get(pk=pk)
    form = TodoForm(instance=todo)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.instance.session_uuid = get_session_key(request)
            form.save()
        return htmx_redirect(request.htmx.current_url)
    return render(request, "fbv_hx_location/todo_item_edit.html", context=locals())


@require_http_methods(["DELETE"])
def todo_delete(request, pk: int):
    todo = Todo.objects.from_session(get_session_key(request)).get(pk=pk)
    todo.delete()
    return htmx_redirect(request.htmx.current_url)


@require_http_methods(["DELETE"])
def todo_clear_completed(request):
    Todo.objects.from_session(get_session_key(request)).completed().delete()
    return htmx_redirect(request.htmx.current_url)
