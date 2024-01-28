import calendar
import datetime

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from apps.calendar.models import Event


class CalendarDay:
    def __init__(self, date, events):
        self.date = date
        self.events: list[Event] = events


def get_calendar_days_by_weeks(year, month, events: list[Event]) -> list[list[CalendarDay]]:
    calendar_days = []

    cal = calendar.Calendar(calendar.MONDAY)
    for date in cal.itermonthdates(year=year, month=month):
        events_for_date = [event for event in events if event.start.date() == date]
        calendar_day = CalendarDay(date, events_for_date)
        calendar_days.append(calendar_day)

    return [calendar_days[i:i + 7] for i in range(0, len(calendar_days), 7)]


def index(request: HttpRequest, year=None, month=None) -> HttpResponse:
    if year is None or month is None:
        year = datetime.date.today().year
        month = datetime.date.today().month

    events = Event.objects.filter(start__year=year, start__month=month).order_by('start')
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
        }
    )
