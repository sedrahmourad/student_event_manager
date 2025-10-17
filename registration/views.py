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
    
    # For GET (List) requests: filter by current user and use the List Serializer
    def get_queryset(self):
        # Filter registrations to only show the currently logged-in user's registrations
        return Registration.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        # Use different serializers based on the request method
        if self.request.method == 'POST':
            return RegistrationCreateSerializer
        return RegistrationListSerializer

    def perform_create(self, serializer):
        """
        Custom creation logic for POST request:
        1. Checks for event existence.
        2. Ensures student hasn't registered already (via unique_together check).
        3. Saves the registration object.
        """
        event_id = self.request.data.get('event_id')
        
        # 1. Check if the event exists
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response(
                {'event_id': ['Event not found.']},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Attempt to create the registration
        try:
            # Pass the currently authenticated user to the serializer for saving
            serializer.save(user=self.request.user, event=event)
        
        except IntegrityError:
            # Handles the unique_together constraint error (already registered)
            return Response(
                {'detail': 'You are already registered for this event.'},
                status=status.HTTP_409_CONFLICT
            )
        except Exception as e:
            # Generic error handling
            return Response(
                {'detail': f'Registration failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationCancelView(generics.DestroyAPIView):
    """
    DELETE /api/registrations/{id}/cancel/ (Student only): Cancel a registration.
    """
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = Registration.objects.all()
    lookup_field = 'pk' # The URL will pass the registration ID (pk)

    def delete(self, request, *args, **kwargs):
        """
        Custom deletion logic: Ensures the student can only delete their own registration.
        """
        # Retrieve the registration instance based on the URL ID
        registration = get_object_or_404(
            self.get_queryset().filter(user=request.user), 
            pk=kwargs['pk']
        )
        
        # Perform deletion
        registration.delete()
        
        return Response(
            {'detail': 'Registration successfully cancelled.'},
            status=status.HTTP_204_NO_CONTENT
        )

