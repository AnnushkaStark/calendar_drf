from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response

from .models import EventModel
from .serializers import EventSerializer, EventCreateSerializer, UpdateEventSerielizer
from .utils import (
    get_repetitions,
    get_date,
    crete_repeat_dates,
    read_events_by_date,
    check_found,
    remove_multi,
)


class ReadEventsView(APIView):
    serializer_class = EventSerializer

    def get(self, *args, **kwargs):
        found_date = get_date(self.kwargs)
        found_events = read_events_by_date(found_date=found_date)
        return found_events


class CreateEventView(APIView):
    queryset = EventModel.objects.all()
    serializer_class = EventCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            repetitions = get_repetitions(event=event)
            crete_repeat_dates(event=event, dates=repetitions)
            return Response(
                {"id": event.id, "name": event.name}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEventView(APIView):
    queryset = EventModel.objects.all()
    serializer_class = UpdateEventSerielizer
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs["id"]
        found_date = get_date(self.kwargs)
        found_event = check_found(event_id=event_id, found_date=found_date)
        if found_event:
            instance = found_event
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class RemoveEventView(APIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"

    def delete(self, *args, **kwargs):
        event_id = self.kwargs["id"]
        found_date = get_date(self.kwargs)
        found_event = check_found(event_id=event_id, found_date=found_date)
        if found_event:
            found_event.dates.remove(found_event)
            found_event.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class RemoveNextEventsView(APIView):
    def post(self, request, *args, **kwargs):
        event_id = kwargs["id"]
        found_date = get_date(self.kwargs)
        found_event = check_found(event_id=event_id, found_date=found_date)
        if found_event:
            remove_multi(found_date=found_date)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class RemoveEventFullView(APIView):
    queryset = EventModel.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"

    def get_object(self, *args, **kwargs):
        event_id = self.kwargs["id"]
        try:
            found_event = EventModel.objects.get(id=event_id)
        except EventModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        found_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
