from rest_framework.serializers import ModelSerializer

from .models import EventModel


class EventSerializer(ModelSerializer):

    class Meta:
        model = EventModel
        fields = "__all__"
