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
from .serializers import EventSerializer
from .tasks import create_repeating_events


class ReadEventsView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        queryset = EventModel.objects.filter(
            date__year=year, date__month=month, date__day=day
        )
        return queryset


class CreateEventView(CreateAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            if event.period:
                create_repeating_events.delay(event.id, event.start_time, event.period)

            return Response({"id": event.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEventView(RetrieveUpdateAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"

    def get_object(self):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        event_id = self.kwargs["id"]
        try:
            event = EventModel.objects.get(
                id=event_id,
                start_at__year=year,
                start_at__month=month,
                start_at__day=day,
            )
        except EventModel.DoesNotExist:
            raise get_object_or_404(EventModel, id=event_id)
        return event

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
        try:
            event = EventModel.objects.get(
                id=event_id,
                start_at__year=year,
                start_at__month=month,
                start_at__day=day,
            )
        except EventModel.DoesNotExist:
            raise get_object_or_404(EventModel, id=event_id)

        return event


class RemoveNextEventsView(APIView):
    def post(self, request, id, year, month, day):
        try:
            current_event = EventModel.objects.get(
                id=id, start_at__year=year, start_at__month=month, start_at__day=day
            )
        except EventModel.DoesNotExist:
            return Response(
                {"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )
        current_event.delete()
        deleted_count, _ = EventModel.objects.filter(
            start_at__gt=current_event.start_time,
            period=current_event.period,
            name=current_event.name,
        ).delete()
        return Response(
            {
                "message": f"Successfully deleted {deleted_count + 1} events starting from the specified date."
            },
            status=status.HTTP_200_OK,
        )
