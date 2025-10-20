# events/views_html.py
from django.shortcuts import render, get_object_or_404
from .models import Event

def event_list_page(request):
    """
    Display all events for students and organizers.
    """
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/events_list.html', {'events': events})

def event_detail_page(request, pk):
    """
    Display a single event’s details.
    """
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})
