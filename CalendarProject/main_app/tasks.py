from celery import shared_task
from django.utils import timezone

from .models import EventModel


@shared_task
def create_recurring_event(event_id):
    event = EventModel.objects.get(id=event_id)
    new_event = EventModel.objects.create(
        name=event.name,
        start_time=event.start_time + timezone.timedelta(days=event.period),
    )
    return new_event
