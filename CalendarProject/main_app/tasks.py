from datetime import timedelta

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import EventModel


@shared_task
def create_repeating_events(event_id, start_time, period):
    event = EventModel.objects.get(id=event_id)
    next_event = EventModel(
        name=event.name,
        start_time=event.start_time + timedelta(days=period),
        period=period,
    )
    next_event.save()
    create_repeating_events.delay(
        args=[next_event.id, next_event.start_time, period], eta=next_event.start_time
    )
