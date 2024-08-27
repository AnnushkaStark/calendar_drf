from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import EventModel
from datetime import datetime, timedelta


class TestCreate(APITestCase):
    url = reverse("create_event")
    data_with_priod = {
        "name": "Event with period",
        "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "period": 7,
        "reccurence_limit": (datetime.now() + timedelta(days=5)).isoformat(),
    }
    data_without_period = {
        "name": "event without period",
        "start_time": (datetime.now() + timedelta(days=5)).isoformat(),
    }
    invalid_data = {"name": "invalid event", "start_time": ""}

    invalid_data_with_period = {
        "name": "Event with period",
        "start_time": (datetime.now() + timedelta(days=3)).isoformat(),
        "period": 7,
    }

    def test_create_event_with_period(self):
        response = self.client.post(self.url, data=self.data_with_priod)
        assert response.status_code == 201
        created_event = EventModel.objects.get(
            name="Event with period",
            period=7,
        )
        assert created_event is not None

    def test_create_event_without_period(self):
        response = self.client.post(self.url, data=self.data_without_period)
        assert response.status_code == 201
        created_event = EventModel.objects.get(name=self.data_without_period["name"])
        assert created_event is not None

    def test_create_evetn_with_invalid_data(self):
        response = self.client.post(self.url, data=self.invalid_data)
        assert response.status_code == 400
        not_created_event = EventModel.objects.filter(
            name=self.invalid_data["name"]
        ).count()
        assert not_created_event == 0

    def test_create_event_with_period_without_reccurence_limit(self):
        response = self.client.post(self.url, self.invalid_data_with_period)
        assert response.status_code == 400
        not_created_event = EventModel.objects.filter(
            name=self.invalid_data["name"]
        ).count()
        assert not_created_event == 0
