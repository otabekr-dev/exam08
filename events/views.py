from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .serializers import EventSerializer, EventRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Count

from .models import Events
from registration.models import Registration

class EventCreateView(CreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class EventRegisterView(CreateAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        event = serializer.validated_data['event']

        serializer.save(user=self.request.user)

        event.capacity -= 1
        event.save()

class EventRegistrationCancelView(DestroyAPIView):
    serializer_class = EventRegistrationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):

        return Registration.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):

        event = instance.event
        event.capacity += 1
        event.save()
        instance.delete()



class EventStatsView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        events_with_regs = Events.objects.annotate(
            registered_count=Count('registrations')
        ).values('id', 'title', 'registered_count', 'capacity')


        for event in events_with_regs:
            event['available_spots'] = event['capacity'] - event['registered_count']


        top_5_events = Events.objects.annotate(
            registered_count=Count('registrations')
        ).order_by('-registered_count')[:5].values('id', 'title', 'registered_count')

        return Response({
            "all_events": list(events_with_regs),
            "top_5_events": list(top_5_events)
        })
