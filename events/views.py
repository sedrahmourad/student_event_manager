from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .serializers import EventSerializer
from .permissions import isOrganizer, isOwnerAndOrganizer


# -----------------------------
# 🔹 API ViewSet for Events
# -----------------------------
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer

    # Permissions based on the action
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated, isOrganizer]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, isOwnerAndOrganizer]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]  # <-- FIXED (was self.permission_classes)

    # Filtering, searching, and ordering setup
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'date', 'location']
    search_fields = ['title', 'description', 'category']

    def perform_create(self, serializer):
        """Automatically set the organizer to the current user when creating an event."""
        serializer.save(organizer=self.request.user)


# -----------------------------
# 🔹 HTML Template Views
# -----------------------------
def event_list_page(request):
    """Render a list of all events for students."""
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/events_list.html', {'events': events})


def event_detail_page(request, event_id):
    """Render details for a single event."""
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})
