from django.urls import path

from . import views

app_name = "todomvc"

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("list/<str:filter_by>", views.todo_list, name="todo_list_with_params"),
    path("toggle/<int:pk>", views.todo_toggle, name="todo_toggle"),
    path("toggle-all", views.todo_toggle_all, name="todo_toggle_all"),
    path("partial-item/<int:pk>", views.todo_partial_item, name="todo_partial_item"),
    path("create", views.todo_create, name="todo_create"),
    path("edit/<int:pk>", views.todo_edit, name="todo_edit"),
    path("delete/<int:pk>", views.todo_delete, name="todo_delete"),
    path("clear-completed", views.todo_clear_completed, name="todo_clear_completed"),
]
