from django.db import models
from django.utils import timezone


class EventModel(models.Model):
    """
    Модель события

    ## Attrs:
        - name: str - название события
        - start_time: datetime - дата и время начала события Unix timestamp
        - period: datetime - периодичность события в днях
    """

    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    period = models.IntegerField()

    def __str__(self):
        return self.name
