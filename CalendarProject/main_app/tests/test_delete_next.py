from django.urls import reverse
from rest_framework.test import APITestCase

from main_app.models import EventModel
from datetime import datetime, timedelta


class TestDeleteNextEvent(APITestCase):
    def setUp(self):
        self.event1 = EventModel.objects.create(
            name="Test Event",
            start_time=(datetime.now() + timedelta(days=2)).isoformat(),
            period=2,
            reccurence_limit=(datetime.now() + timedelta(days=5)),
        )
        self.event2 = EventModel.objects.create(
            name="Test Event",
            start_time=(datetime.now() + timedelta(days=9)).isoformat(),
            period=2,
            reccurence_limit=(datetime.now() + timedelta(days=5)),
        )
        self.event3 = EventModel.objects.create(
            name="Test Event",
            start_time=(datetime.now() + timedelta(days=16)).isoformat(),
            period=2,
            reccurence_limit=(datetime.now() + timedelta(days=5)),
        )

    def Qtest_delete_events_succsess(self):
        url = reverse(
            "remove_next_events", kwargs={"id": 1, "year": 2024, "month": 8, "day": 29}
        )
        response = self.client.post(url)
        assert response.status_code == 200

    # deleted_events = EventModel.objects.filter(name="Test Event", period=7).count()
