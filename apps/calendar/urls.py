from django.urls import path

from apps.calendar import views

app_name = "calendar"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:year>/<int:month>", views.index, name="index_by_year_month"),
    path("events/add-modal", views.event_add_modal, name="event_add_modal"),
    path("events/<int:pk>/edit-modal", views.event_edit_modal, name="event_edit_modal"),
    path("events/<int:pk>/delete-modal", views.event_delete_modal, name="event_delete_modal"),
]
