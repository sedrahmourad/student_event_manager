from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import Registration
from .serializers import RegistrationCreateSerializer, RegistrationListSerializer
from .permissions import IsStudent

# You will need to import the Event model to perform lookups
# Use the string reference here, or handle the import carefully
from events.models import Event # Assuming 'events' is set up correctly

class RegistrationListCreateView(generics.ListCreateAPIView):
    """
    POST /api/registrations/ (Student only): Register for an event.
    GET /api/registrations/ (Student only): List the student's registered events.
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegistrationCreateSerializer
        return RegistrationListSerializer

    def create(self, request, *args, **kwargs):
        """Custom POST logic with clean JSON responses."""
        event_id = request.data.get('event_id')

        # 1️⃣ Check if the event exists
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response(
                {'error': 'Event not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2️⃣ Try creating a registration
        try:
            registration = Registration.objects.create(
                user=request.user,
                event=event
            )
            serializer = RegistrationListSerializer(registration)
            return Response(
                {
                    'message': 'Registration successful!',
                    'registration': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except IntegrityError:
            # Student already registered
            return Response(
                {'error': 'You are already registered for this event.'},
                status=status.HTTP_409_CONFLICT
            )

        except Exception as e:
            return Response(
                {'error': f'Registration failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationCancelView(generics.DestroyAPIView):
    """
    DELETE /api/registrations/{id}/cancel/ (Student only): Cancel a registration.
    """
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = Registration.objects.all()
    lookup_field = 'pk'  # The URL will pass the registration ID (pk)

    def delete(self, request, *args, **kwargs):
        """
        Custom deletion logic: Ensures the student can only delete their own registration.
        """
        registration = get_object_or_404(
            self.get_queryset().filter(user=request.user),
            pk=kwargs['pk']
        )
        registration.delete()
        return Response(
            {'detail': f'Registration for event \"{registration.event.title}\" cancelled successfully.'},
            status=status.HTTP_200_OK
        )

