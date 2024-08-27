from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import EventModel
from datetime import datetime, timedelta


class TestDeleteOneEvent(APITestCase):
    def setUp(self):
        self.event1 = EventModel.objects.create(
            name="Test Event",
            start_time=(datetime.now() + timedelta(days=2)).isoformat(),
            period=7,
        )

    def test_delete_event_succsess(self):
        url = reverse(
            "remove_event", kwargs={"id": 1, "year": 2024, "month": 8, "day": 29}
        )
        response = self.client.delete(url)
        assert response.status_code == 204

    def test_delete_event_with_invalid_id(self):
        url = reverse(
            "remove_event", kwargs={"id": 404, "year": 2024, "month": 8, "day": 29}
        )
        response = self.client.delete(url)
        assert response.status_code == 404
