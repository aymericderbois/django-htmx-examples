from django.urls import path

from apps.calendar import views

app_name = "calendar"

urlpatterns = [
    path("", views.index, name="index"),
    path("/<int:year>/<int:month>", views.index, name="index_by_year_month"),
]
