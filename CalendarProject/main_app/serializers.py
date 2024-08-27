from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import EventModel


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventModel
        fields = "__all__"


class EventCreateSerializer(serializers.ModelSerializer):
    period = serializers.IntegerField(allow_null=True)
    recurrence_limit = serializers.DateTimeField

    def validate(self, data):
        if data.get("period") is not None:
            if data.get("recurrence_limit") is None:
                raise ValidationError(
                    "recurrence_limit is required when period is None"
                )

        return data

    class Meta:
        model = EventModel
        fields = "__all__"
