import time

from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch

from main_app.models import EventModel
from datetime import datetime, timedelta


class TestCreate(APITestCase):
    url = reverse("create_event")
    data_with_priod = {
        "name": "Event with period",
        "start_time": (datetime.now() + timedelta(days=3)).isoformat(),
        "period": 7,
    }
    data_without_period = {
        "name": "event without period",
        "start_time": (datetime.now() + timedelta(days=5)).isoformat(),
    }
    invalid_data = {"name": "invalid event", "start_time": ""}

    @patch("main_app.tasks.create_repeating_events.delay")
    def test_create_event_with_period(self, mock_create_repeating_events):
        response = self.client.post(self.url, data=self.data_with_priod)
        assert response.status_code == 201
        created_event_first = EventModel.objects.get(name="Event with period", period=7)
        assert created_event_first is not None
        time.sleep(5)
        mock_create_repeating_events.assert_any_call(
            created_event_first.id, created_event_first.start_time, 7
        )

    @patch("main_app.tasks.create_repeating_events.delay")
    def test_create_event_without_period(self, mock_create_repeating_events):
        response = self.client.post(self.url, data=self.data_without_period)
        assert response.status_code == 201
        created_event = EventModel.objects.get(name=self.data_without_period["name"])
        assert created_event is not None
        mock_create_repeating_events.assert_not_called()

    def test_create_evetn_with_invalid_data(self):
        response = self.client.post(self.url, data=self.invalid_data)
        assert response.status_code == 400
        not_created_event = EventModel.objects.filter(
            name=self.invalid_data["name"]
        ).count()
        assert not_created_event == 0
