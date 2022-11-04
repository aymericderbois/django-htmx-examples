from django.urls import path

from todomvc.cbv_hx_location.views import (
    TodoListView,
    TodoActiveListView,
    TodoCompletedListView,
    TodoToggleView,
    TodoToggleAllView,
    TodoClearCompletedView,
    TodoDeleteView,
    TodoCreateView,
    TodoUpdateView,
    TodoItemPartialView,
)

app_name = "todo"

urlpatterns = [
    path(
        "list",
        TodoListView.as_view(),
        name="list-all",
    ),
    path(
        "list/active",
        TodoActiveListView.as_view(),
        name="list-active",
    ),
    path(
        "list/completed",
        TodoCompletedListView.as_view(),
        name="list-completed",
    ),
    path(
        "toggle-all",
        TodoToggleAllView.as_view(),
        name="toggle-all",
    ),
    path(
        "partial/item/<int:pk>",
        TodoItemPartialView.as_view(),
        name="item-partial",
    ),
    path(
        "partial/item/<int:pk>/edit",
        TodoUpdateView.as_view(),
        name="item-edit-partial",
    ),
    path(
        "clear-completed",
        TodoClearCompletedView.as_view(),
        name="clear-completed",
    ),
    path(
        "cvb/<int:pk>/toggle",
        TodoToggleView.as_view(),
        name="toggle",
    ),
    path(
        "cvb/<int:pk>/delete",
        TodoDeleteView.as_view(),
        name="delete-view",
    ),
    path(
        "cvb/create",
        TodoCreateView.as_view(),
        name="create",
    ),
]
