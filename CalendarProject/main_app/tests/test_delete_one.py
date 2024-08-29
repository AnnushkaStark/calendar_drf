from datetime import timedelta

from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import EventModel

from datetime import datetime, timedelta
from ..utilies.other import get_repetitions


class TestDeleteOneEvent(APITestCase):
    def setUp(self):
        self.event1 = EventModel.objects.create(
            name="Test Event",
            start_time=(datetime.now() + timedelta(days=2)),
            period=7,
            reccurence_limit=(datetime.now() + timedelta(days=15)),
        )

    def Qtest_delete_event_succsess(self):
        url = reverse(
            "remove_event",
            kwargs={
                "year": self.event1.start_time.year,
                "month": self.event1.start_time.month,
                "day": self.event1.start_time.day,
                "id": 1,
            },
        )
        response = self.client.delete(url)
        assert response.status_code == 204

    def Qtest_delete_event_with_invalid_id(self):
        url = reverse(
            "remove_event", kwargs={"id": 404, "year": 2024, "month": 8, "day": 29}
        )
        response = self.client.delete(url)
        assert response.status_code == 404
