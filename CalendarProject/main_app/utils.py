from typing import List, Optional
from datetime import datetime

from .models import EventModel


def get_events_by_date(
    current_date: datetime, found_date: datetime
) -> List[EventModel]:
    if found_date == current_date:
        found_events = EventModel.objects.filter(start_time=found_date)
        return found_events
    if found_date > current_date:
        found_events = EventModel.objects.filter(
            start_time__gte=current_date, start_time__lte=found_date
        )
        return found_events
    if found_date < current_date:
        found_events = EventModel.objects.filter(
            start_time__gte=found_date, start_time__lte=current_date
        )
        return found_events


def delete_repetitions_next(event: EventModel, found_date: datetime) -> List:
    repetitions = event.get_repetitions(event.start_time)
    for date in repetitions:
        if date > found_date:
            repetitions.remove(date)
    return repetitions


def delete_repetition_one_by_date(event: EventModel, found_date: datetime) -> List:
    repetitions = event.get_repetitions(event.start_time)
    repetitions = repetitions.remove(found_date)
    return repetitions


def check_found(found_date: datetime, event_id: int) -> Optional[EventModel]:
    if found_event := EventModel.objects.get(id=event_id):
        if found_event.period:
            repetitions = found_event.get_repetitions(found_event.start_time)
            if found_date in repetitions:
                return found_event
        if found_event.start_time == found_date:
            return found_event
