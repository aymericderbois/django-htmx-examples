from django.contrib import admin

from apps.calendar.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start", "end")
