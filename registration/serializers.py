from rest_framework import serializers
from .models import Registration
class EventSummarySerializer(serializers.Serializer):
    #used to return summarized event data 
    title = serializers.CharField()
    description = serializers.CharField()
    date = serializers.DateTimeField(allow_null=True)
    end_date = serializers.DateTimeField(allow_null=True)
    location = serializers.CharField()
    category = serializers.CharField()
    event_id = serializers.IntegerField(source='pk')

class RegistrationCreateSerializer(serializers.ModelSerializer):
    # for creating a new registration (POST) onlu using event_id
    event_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Registration
        fields = ('event_id',)
    def create(self, validated_data):
        return Registration.objects.create(**validated_data)
class RegistrationListSerializer(serializers.ModelSerializer):
    # for listing student registration (GET)
    event = EventSummarySerializer(read_only=True)
    class Meta:
        model = Registration
        fields = ('id', 'event', 'timestamp',)
        read_only_fields = ('id', 'event', 'timestamp',)
        
