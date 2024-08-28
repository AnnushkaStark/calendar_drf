from django.db import models


class DateModel(models.Model):
    """
    Модель даты повторения события
    ## Attrs
        - date: datetime - дата повторения события
        - events: List[EventDateRelated] - связь m2m даты повторения событий
    """

    date = models.DateTimeField()
    events = models.ManyToManyField("EventModel", related_name="events_at_date")

    def __str__(self):
        return f"{self.date}"
