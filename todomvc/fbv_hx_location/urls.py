from django.urls import path

from . import views

app_name = "fbv_hx_location"

urlpatterns = [
    path("list", views.todo_list, name="todo_list"),
    path("list/active", views.todo_list_active, name="todo_list_active"),
    path("list/completed", views.todo_list_completed, name="todo_list_completed"),
    path("toggle/<int:pk>", views.todo_toggle, name="todo_toggle"),
    path("toggle-all", views.todo_toggle_all, name="todo_toggle_all"),
    path("partial-item/<int:pk>", views.todo_partial_item, name="todo_partial_item"),
    path("create", views.todo_create, name="todo_create"),
    path("edit/<int:pk>", views.todo_edit, name="todo_edit"),
    path("delete/<int:pk>", views.todo_delete, name="todo_delete"),
    path("clear-completed", views.todo_clear_completed, name="todo_clear_completed"),
]
