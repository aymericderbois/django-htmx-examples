import calendar
import datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseLocation

from apps.calendar.forms import EventForm
from apps.calendar.models import Event


class CalendarDay:
    def __init__(self, date, events):
        self.date: datetime.date = date
        self.events: list[Event] = events


def get_calendar_days_by_weeks(
    year, month, events: list[Event]
) -> list[list[CalendarDay]]:
    calendar_days = []

    cal = calendar.Calendar(calendar.MONDAY)
    for date in cal.itermonthdates(year=year, month=month):
        events_for_date = [event for event in events if event.start.date() == date]
        calendar_day = CalendarDay(date, events_for_date)
        calendar_days.append(calendar_day)

    return [calendar_days[i : i + 7] for i in range(0, len(calendar_days), 7)]


def index(request: HttpRequest, year=None, month=None) -> HttpResponse:
    if year is None or month is None:
        year = datetime.date.today().year
        month = datetime.date.today().month

    events = Event.objects.filter(start__year=year, start__month=month).order_by(
        "start"
    )
    next_month_date = datetime.date(year, month, 1) + datetime.timedelta(days=35)
    previous_month_date = datetime.date(year, month, 1) - datetime.timedelta(days=10)

    return render(
        request,
        "calendar/index.html",
        context={
            "calendar": calendar.Calendar(calendar.MONDAY),
            "today": datetime.date.today(),
            "weeks": get_calendar_days_by_weeks(year, month, events),
            "next_month_date": next_month_date.replace(day=1),
            "previous_month_date": previous_month_date.replace(day=1),
            "year": year,
            "month": month,
        },
    )


@require_http_methods(["GET", "POST"])
def event_add_modal(request) -> HttpResponse:
    given_date = request.GET.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    form = EventForm(request.POST or None, initial={"start": given_date})
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseLocation(request.htmx.current_url)
    return render(
        request,
        "calendar/event_add_modal.html",
        context={"form": form, "form_url": reverse("calendar:event_add_modal")},
    )


@require_http_methods(["GET", "POST"])
def event_edit_modal(request, pk: int) -> HttpResponse:
    form = EventForm(request.POST or None, instance=get_object_or_404(Event, pk=pk))
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponseLocation(request.htmx.current_url)
    return render(
        request,
        "calendar/event_add_modal.html",
        context={
            "form": form,
            "form_url": reverse("calendar:event_edit_modal", kwargs={"pk": pk}),
        },
    )


@require_http_methods(["GET", "DELETE"])
def event_delete_modal(request, pk: int) -> HttpResponse:
    event = get_object_or_404(Event, pk=pk)
    if request.method == "DELETE":
        event.delete()
        return HttpResponseLocation(request.htmx.current_url)

    return render(
        request, "calendar/event_delete_confirm_modal.html", context={"event": event}
    )
