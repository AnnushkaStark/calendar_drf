from datetime import datetime
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    DestroyAPIView,
)
from rest_framework import status
from rest_framework.response import Response

from .models import EventModel
from .serializers import EventSerializer, EventCreateSerializer
from .utils import (
    get_events_by_date,
    delete_repetitions_next,
    check_found,
    delete_repetition_one_by_date,
)


class ReadEventsView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self, *args, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        current_date = datetime.now().date()
        found_date = datetime(year=year, month=month, day=day)
        queryset = []
        found_events = get_events_by_date(
            current_date=current_date, found_date=found_date
        )
        for event in found_events:
            repetitions = event.get_repetitions(event.start_time)
            if found_date in repetitions:
                queryset.append({"name": event.name, "start_time": found_date})
        return queryset


class CreateEventView(CreateAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            return Response({"id": event.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEventView(RetrieveUpdateAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventCreateSerializer
    lookup_field = "id"

    def get_object(self, *args, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        event_id = self.kwargs["id"]
        found_date = datetime(year=year, month=month, day=day)
        try:
            found_event = check_found(event_id=event_id, found_date=found_date)
        except EventModel.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return found_event

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveEventView(DestroyAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"

    def get_object(self):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        event_id = self.kwargs["id"]
        found_date = datetime(year=year, month=month, day=day)
        try:
            found_event = check_found(event_id=event_id, found_date=found_date)
            delete_repetition_one_by_date(event=found_event, found_date=found_date)
        except EventModel.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return found_event


class RemoveNextEventsView(APIView):
    def post(self, request, id, year, month, day):
        try:
            found_date = datetime(year=year, month=month, day=day)
            current_event = check_found(found_date=found_date, event_id=id)
        except EventModel.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        delete_repetitions_next(event=current_event, found_date=found_date)
        current_event.delete()
        return Response(status=status.HTTP_200_OK)


class RemoveEventFullView(DestroyAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"

    def get_object(self, *args, **kwargs):
        event_id = self.kwargs["id"]
        try:
            found_event = EventModel.objects.get(id=event_id)
        except EventModel.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return found_event
