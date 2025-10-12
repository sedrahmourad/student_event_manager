from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .serializers import EventSerializer # Assume you've created this
from .permissions import isOrganizer, isOwnerAndOrganizer # Import the custom permissions
# Create your views here.

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permissions 
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated, isOrganizer]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, isOwnerAndOrganizer]
        else:
            permission_classes = [permissions.AllowAny]
        return [permissions() for permission in permission_classes]
# --- Filtering and Searching ---
    
    # 1. Allows filtering using query parameters like ?category=Tech or ?date=2025-10-01
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # 2. Fields available for exact filtering
    filterset_fields = ['category', 'date', 'location']
    
    # 3. Fields available for fuzzy search (useful for title/description)
    search_fields = ['title', 'description', 'category']
    
    # --- Custom Logic ---

    def perform_create(self, serializer):
        """Saves the organizer field to the event upon creation."""
        # When an organizer creates an event, the 'organizer' field is automatically set to the request user.
        serializer.save(organizer=self.request.user)
