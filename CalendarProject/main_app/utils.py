from typing import List, Optional
from datetime import datetime

from django.db.models import Q
from django.utils import timezone


from .models import EventModel, EventDate


def get_repetitions(event: EventModel) -> List[datetime]:
    """
    Генерация дат повторений
    от даты начала события до даты лимита повторов
    """
    repetitions = []
    if event.period and event.reccurence_limit:
        date = event.start_time
        while (date + timezone.timedelta(days=event.period)) <= event.reccurence_limit:
            repetitions.append(date)
            date += timezone.timedelta(days=event.period)
        return repetitions


def crete_repeat_dates(event: EventModel, dates: List[datetime]|None) -> List[EventDate]:
    if dates:
        for _ in range(len(dates)):
            event_dates = EventDate.objects.bulk_create(dates, batch_size=1000)
            return event_dates


def check_found(found_date: datetime, event_id: int) -> Optional[EventModel]:
    """
    Проверка найденного события тк возможен не только выбора даты создание
    события но и одной из дат его повторов
    """
    found_event = (
        EventModel.objects.prefetch_related("dates")
        .filter(
            Q(dates__date=found_date.date(), id=event_id)
            |Q(start_time=found_date.date(), id=event_id)
        )
        .first()
    )
    if found_event:
        return found_event


def read_events_by_date(found_date: datetime) -> List[dict]:
    found_events = (
        EventModel.objects.prefetch_related("dates")
        .filter(Q (start_time=found_date.date())| Q(dates__date=found_date.date()))
    ).all()
    print(found_events)
    queryset = []
    for event in found_events:
        if event.start_time == found_date:
            queryset.append({"neme": event.name, "start_time": event.start_time})
        queryset.append({"neme": event.name, "start_time": found_date})
    return queryset


def get_date(data: dict) -> datetime:
    """
    получение даты из **kwargs эндпонйтов
    """
    year = data["year"]
    month = data["month"]
    day = data["day"]
    return datetime(year=year, month=month, day=day)


def remove_multi(found_date: datetime) -> None:
    deletd_dates = EventModel.objects.prefetch_related("dates").delete(
        dates__gte=found_date
    )
    return deletd_dates
