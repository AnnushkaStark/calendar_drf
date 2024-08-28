from typing import List
from datetime import datetime

from django.utils import timezone

from ..models.date import DateModel
from ..models.event import EventModel


def create_repetitions(
    repetitions: List[datetime], event: EventModel
) -> List[DateModel]:
    """
    Создание дат повторов события
    """
    if repetitions:
        objects = [DateModel(date=(repetition for repetition in repetitions))]
        for _ in range(len(repetitions)):
            db_objects = DateModel.objects.bulk_create(objects, batch_size=1000)
        return db_objects
