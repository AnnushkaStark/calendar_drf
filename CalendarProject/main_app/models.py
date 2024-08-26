from django.db import models

from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class EventModel(models.Model):
    """
    Модель события

    ## Attrs:
        - name: str - название события
        - start_time: int - дата и время начала события Unix timestamp
        - period: datetime - периодичность события в днях
        - task_id - идентификатор события (задача селери)
            для повторяющихся событий
    """

    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    period = models.IntegerField()

    def __str__(self):
        return self.name
