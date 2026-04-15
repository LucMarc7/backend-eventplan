from rest_framework.serializers import ModelSerializer
from events.models import Mariage, Category, Event, BirthDay, Concert, Conference



class EventCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"




class EventImageSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_image']
        read_only_fields = ['id']


# Event Mariage Serializers

class MariageSerializer(ModelSerializer):
    class Meta:
        model = Mariage
        fields = "__all__"


# Event Birthday Serializers

class BirthDaySerializer(ModelSerializer):
    class Meta:
        model = BirthDay
        fields = "__all__"


# Event Concert Serializers

class ConcertSerializer(ModelSerializer):
    class Meta:
        model = Concert
        fields = "__all__"


# Event Conference Serializer

class ConferenceSerializer(ModelSerializer):
    class Meta:
        model = Conference
        fields = "__all__"