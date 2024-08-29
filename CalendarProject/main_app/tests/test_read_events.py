from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import EventModel
from datetime import datetime, timedelta


class TestReadEventsView(APITestCase):
    def setUp(self):
        self.event1 = EventModel.objects.create(
            name="Test Event",
            start_time=(datetime.now() + timedelta(days=2)),
            period=7,
            reccurence_limit=(datetime.now() + timedelta(days=15)),
        )
        self.event2 = EventModel.objects.create(
            name="Another Test Event",
            start_time=(datetime.now() + timedelta(days=3)),
            period=7,
            reccurence_limit=(datetime.now() + timedelta(days=51)),
        )

    def test_get_events_by_date(self):
        url = reverse(
            "events_by_date",
            kwargs={
                "year": self.event1.start_time.year,
                "month": self.event1.start_time.month,
                "day": self.event1.start_time.day,
            },
        )
        response = self.client.get(url)

        assert response.status_code == 200
        assert "TestEvent" in response

    def test_get_next_event(self):
        url = reverse(
            "events_by_date",
            kwargs={
                "year": self.event2.start_time.year,
                "month": self.event2.start_time.month,
                "day": self.event2.start_time.day,
            },
        )
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json()[0]["name"] == "Another Test Event"

    def Qtest_empty_result(self):
        url = reverse("events_by_date", kwargs={"year": 2023, "month": 5, "day": 31})
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.json()) == 0
