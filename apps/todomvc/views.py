from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from apps.todomvc.form import TodoForm
from apps.todomvc.models import Todo
from apps.core.shortcuts import htmx_redirect


@require_http_methods(["GET"])
def todo_list(request, filter_by="all"):
    if filter_by not in ["active", "completed", "all"]:
        raise Http404()

    qs = Todo.objects.from_session(request.todo_session_uuid).order_by("-created_at")

    todos = qs.all().by_status(filter_by)

    number_todo_active = qs.active().count()
    number_todo_completed = qs.completed().count()
    number_todo_total = number_todo_completed + number_todo_active

    return render(
        request,
        "todomvc/todo_list.html",
        context={
            "todos": todos,
            "number_todo_total": number_todo_total,
            "number_todo_active": number_todo_active,
            "number_todo_completed": number_todo_completed,
            "form": TodoForm(),
        },
    )


@require_http_methods(["POST"])
def todo_toggle(request, pk: int):
    todo = get_object_or_404(Todo, session_uuid=request.todo_session_uuid, pk=pk)
    todo.is_done = not todo.is_done
    todo.save()
    return htmx_redirect(request.htmx.current_url)


@require_http_methods(["POST"])
def todo_toggle_all(request):
    Todo.objects.toggle_all(request.todo_session_uuid)
    return htmx_redirect(request.htmx.current_url)


@require_http_methods(["GET"])
def todo_partial_item(request, pk: int):
    return render(
        request,
        "todomvc/todo_item.html",
        {
            "todo": get_object_or_404(
                Todo,
                session_uuid=request.todo_session_uuid,
                pk=pk,
            )
        },
    )


@require_http_methods(["POST"])
def todo_create(request):
    form = TodoForm(request.POST)
    if form.is_valid():
        form.save(session_uuid=request.todo_session_uuid)
    return htmx_redirect(request.htmx.current_url)


@require_http_methods(["GET", "POST"])
def todo_edit(request, pk: int):
    todo = get_object_or_404(Todo, session_uuid=request.todo_session_uuid, pk=pk)
    form = TodoForm(instance=todo, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save(session_uuid=request.todo_session_uuid)
        return htmx_redirect(request.htmx.current_url)

    return render(
        request,
        "todomvc/todo_item_edit.html",
        context={"todo": todo, "form": form},
    )


@require_http_methods(["DELETE"])
def todo_delete(request, pk: int):
    get_object_or_404(Todo, session_uuid=request.todo_session_uuid, pk=pk).delete()
    return htmx_redirect(request.htmx.current_url)


@require_http_methods(["DELETE"])
def todo_clear_completed(request):
    Todo.objects.from_session(request.todo_session_uuid).completed().delete()
    return htmx_redirect(request.htmx.current_url)
