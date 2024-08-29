from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import EventModel
from datetime import datetime, timedelta


class TestUpdateEvent(APITestCase):
    def setUp(self):
        self.event1 = EventModel.objects.create(
            name="Test Event",
            start_time=(datetime.now() + timedelta(days=2)).isoformat(),
            period=7,
        )

    def Qtest_update_event_succsess(self):
        url = reverse(
            "update_event", kwargs={"id": 1, "year": 2024, "month": 8, "day": 29}
        )
        data = {
            "name": "New Name",
        }
        response = self.client.patch(url, data=data)
        assert response.status_code == 200
        updated_event = EventModel.objects.get(id=1)
        assert updated_event.name == "New Name"

    def Qtest_update_event_with_invalid_id(self):
        url = reverse(
            "update_event", kwargs={"id": 4, "year": 2024, "month": 8, "day": 29}
        )
        data = {
            "name": "New Name",
        }
        response = self.client.patch(url, data=data)
        assert response.status_code == 404
        not_updated_event = EventModel.objects.get(id=1)
        assert not_updated_event.name == "Test Event"
