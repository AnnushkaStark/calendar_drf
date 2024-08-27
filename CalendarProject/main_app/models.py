from django.db import models
from django.utils import timezone


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

    def get_repetitions(self, date):
        """
        функция генерирующая даты повторений
        от даты начала события до даты лимита повторов
        """
        repetitions = []
        if self.period and self.reccurence_limit:
            date = self.start_time
            while self.start_time < self.reccurence_limit:
                repetitions.append(date)
                date += timezone.timedelta(days=self.period)
            return repetitions
