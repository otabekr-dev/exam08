from rest_framework import serializers
from .models import Events
from registration.models import Registration

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

    def validate(self, attrs):
        start = attrs.get('start_time')
        end = attrs.get('end_time')
        location = attrs.get('location')
        event_type = attrs.get('event_type')

        if start and end and start >= end:
            raise serializers.ValidationError('End time must be after start time')

        
        if event_type == Events.Event_Type.OFFLINE and not location:
            raise serializers.ValidationError({
                'location': 'Offline event uchun location kiritilishi majburiy'
            })

        return attrs



class EventRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Registration
        fields = ['id','event']

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        event = attrs['event']

        if event.capacity == 0:
            raise serializers.ValidationError('Registration closed')

        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError('Already registered')

        if event.registrations.count() >= event.capacity:
            raise serializers.ValidationError('Event is full')

        return attrs

