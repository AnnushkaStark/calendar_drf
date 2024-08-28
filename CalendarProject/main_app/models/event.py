from django.db import models


class EventModel(models.Model):
    """
    Модель события

    ## Attrs:
        - name: str - название события
        - start_time: datetime - дата и время начала события
        - period: int - периодичность события в днях
        - reccurence_limit: datetime - до какой даты должна повторяться
        - repetitions: - связь m2m даты повторения событий
    """

    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    period = models.IntegerField(null=True, blank=True)
    reccurence_limit = models.DateTimeField(null=True, blank=True)
    repetitions = models.ManyToManyField("DateModel", related_name="event_dates")

    def __str__(self):
        return self.name
