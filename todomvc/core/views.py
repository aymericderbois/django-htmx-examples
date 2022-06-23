import uuid

from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin, DetailView

from todomvc.core.form import TodoForm, TodoUpdateForm
from todomvc.core.models import Todo


def get_session_key(request):
    """Get or create a todolist for the current session."""
    session_uuid = request.session.get("todo_uuid", str(uuid.uuid4()))
    request.session["todo_uuid"] = session_uuid
    return session_uuid


def htmx_redirect(url):
    return HttpResponse(
        content="",
        status=204,
        headers={"HX-Location": url},
    )


class TodoSessionMixin:
    def get_session_todo_queryset(self):
        return Todo.objects.filter(session_uuid=get_session_key(self.request))

    def get_queryset(self):
        return self.get_session_todo_queryset().order_by("-created_at")


class TodoListView(TodoSessionMixin, ListView):
    extra_context = {"menu": "all"}

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["number_todo_active"] = self.get_queryset().filter(is_done=False).count()
        ctx["number_todo_completed"] = self.get_queryset().filter(is_done=True).count()
        ctx["number_todo_total"] = ctx["number_todo_active"] + ctx["number_todo_completed"]
        ctx["number_todo"] = len(self.object_list)
        ctx["form"] = TodoForm()
        return ctx


class TodoActiveListView(TodoListView):
    extra_context = {"menu": "active"}

    def get_queryset(self):
        return super().get_queryset().filter(is_done=False)


class TodoCompletedListView(TodoListView):
    extra_context = {"menu": "completed"}

    def get_queryset(self):
        return super().get_queryset().filter(is_done=True)


class TodoToggleView(TodoSessionMixin, SingleObjectMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.htmx:
            raise Http404()

        todo = self.get_object()
        todo.is_done = not todo.is_done
        todo.save()
        return htmx_redirect(request.htmx.current_url)


class TodoToggleAllView(TodoSessionMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.htmx:
            raise Http404()

        qs = self.get_queryset()

        if qs.filter(is_done=False).count() == 0:
            qs.update(is_done=False)
        else:
            qs.update(is_done=True)

        return htmx_redirect(request.htmx.current_url)


class TodoItemPartialView(TodoSessionMixin, DetailView):
    template_name = "core/todo_item.html"


class TodoDeleteView(TodoSessionMixin, SingleObjectMixin, View):
    def delete(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.delete()
        return htmx_redirect(request.htmx.current_url)


class TodoClearCompletedView(TodoSessionMixin, View):
    def delete(self, request, *args, **kwargs):
        if not request.htmx:
            raise Http404()

        self.get_queryset().filter(is_done=True).delete()

        return htmx_redirect(request.htmx.current_url)


class TodoCreateView(CreateView):
    form_class = TodoForm

    def get(self, request, *args, **kwargs):
        """Create view is only used for saving data, not for displaying form"""
        raise Http404()

    def form_valid(self, form):
        form.instance.session_uuid = get_session_key(self.request)
        form.save()
        return htmx_redirect(self.request.htmx.current_url)

    def form_invalid(self, form):
        # Dont handle form error for now.
        return htmx_redirect(self.request.htmx.current_url)


class TodoUpdateView(TodoSessionMixin, UpdateView):
    form_class = TodoUpdateForm
    template_name = "core/todo_item_edit.html"

    def form_valid(self, form):
        form.save()
        return htmx_redirect(self.request.htmx.current_url)

    def form_invalid(self, form):
        # Dont handle form error for now.
        return htmx_redirect(self.request.htmx.current_url)
