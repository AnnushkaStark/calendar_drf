from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import EventModel
from datetime import datetime, timedelta


class TestReadEventsView(APITestCase):
    def setUp(self):
        self.event1 = EventModel.objects.create(
            name="Test Event",
            start_time=(datetime.now() + timedelta(days=2)).isoformat(),
            period=7,
        )
        self.event2 = EventModel.objects.create(
            name="Another Test Event",
            start_time=(datetime.now() + timedelta(days=3)).isoformat(),
            period=7,
        )

    def test_get_events_by_date(self):
        url = reverse("events_by_date", kwargs={"year": 2024, "month": 8, "day": 29})
        response = self.client.get(url)

        assert response.status_code == 200

        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Test Event"

    def test_get_next_event(self):
        url = reverse("events_by_date", kwargs={"year": 2024, "month": 8, "day": 30})
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Another Test Event"

    def test_empty_result(self):
        url = reverse("events_by_date", kwargs={"year": 2023, "month": 5, "day": 31})
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.json()) == 0
