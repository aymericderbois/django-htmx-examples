from django.urls import path, include

from todomvc.core.views import (
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
        "list/",
        include(
            (
                [
                    path("", TodoListView.as_view(), name="all"),
                    path("active", TodoActiveListView.as_view(), name="active"),
                    path("completed", TodoCompletedListView.as_view(), name="completed"),
                    path("toggle-all", TodoToggleAllView.as_view(), name="toggle-all"),
                    path("partial/item/<int:pk>", TodoItemPartialView.as_view(), name="item-partial"),
                    path("partial/item/<int:pk>/edit", TodoUpdateView.as_view(), name="item-edit-partial"),
                    path("clear-completed", TodoClearCompletedView.as_view(), name="clear-completed"),
                ],
                "list",
            )
        ),
    ),
    path("<int:pk>/toggle", TodoToggleView.as_view(), name="toggle"),
    path("<int:pk>/delete", TodoDeleteView.as_view(), name="delete-view"),
    path("create", TodoCreateView.as_view(), name="create"),
]
