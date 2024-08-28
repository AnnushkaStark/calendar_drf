from django.db import models


class EventModel(models.Model):
    """
    Модель события

    ## Attrs:
        - name: str - название события
        - start_time: datetime - дата и время начала события
        - period: int - периодичность события в днях
        - reccurence_limit: datetime - до какой даты событе должно повторяться
    """

    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    period = models.IntegerField(null=True, blank=True)
    reccurence_limit = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class DateModel(models.Model):
    """
    Модель даты повторения события
    ## Attrs
        - date: datetime - дата повторения события
    """

    date = models.DateTimeField()


class EventDateRelated(models.Model):
    """
    Родственная модель связи (события и даты повторения)
    ## Attrs:
        event: FK связь EventModel
        repeat_date: FK связь DateModel
    """

    event = models.ForeignKey(
        EventModel, on_delete=models.CASCADE, related_name="event_dates"
    )
    repeat_date = models.ForeignKey(
        DateModel, on_delete=models.CASCADE, related_name="events"
    )

    class Meta:
        unique_together = ("event", "repeat_date")
