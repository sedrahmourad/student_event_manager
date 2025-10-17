from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Registration

# Import settings for email configuration
from django.conf import settings 

# Signal handler function: runs whenever a Registration object is saved (created or updated)
@receiver(post_save, sender=Registration)
def send_registration_confirmation(sender, instance, created, **kwargs):
    """
    Sends a confirmation email and prepares data for Calendar API/Link 
    when a new Registration is created.
    """
    # Only run the code if a new registration object was created
    if created:
        registration = instance
        user = registration.user
        event = registration.event

        # 1. Create the Google Calendar Link (iCal format is simplest for a link)
        # Note: For full integration, you would use the google-api-python-client library here
        # after handling the student's OAuth flow, but this link is a good starting point.
        calendar_link = generate_google_calendar_link(event)

        # 2. Build the Email Content
        subject = f'✅ Confirmed: You are registered for {event.title}'
        
        # We will use an HTML template for a nice email design
        html_message = render_to_string('registration/email/registration_confirmation.html', {
            'user': user,
            'event': event,
            'calendar_link': calendar_link
        })
        
        # A plain text version for email clients that don't support HTML
        plain_message = strip_tags(html_message)
        
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        # 3. Send the Email
        try:
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            print(f"Successfully sent confirmation email to {to_email}")
        except Exception as e:
            # Important: Log the error instead of failing the user's registration
            print(f"Error sending email to {to_email}: {e}")


def generate_google_calendar_link(event):
    """Generates a Google Calendar URL for easy adding of the event.
    
    ASSUMES: The Event model now has an 'end_date' field for accuracy.
    """
    
    # Format start and end date/time strings for Google Calendar URL (ZULU format)
    start_time = event.date.strftime('%Y%m%dT%H%M%S')
    
    # *** CHANGE: Use the actual event.end_date field ***
    # This now assumes event.end_date exists and is a DateTimeField
    end_time = event.end_date.strftime('%Y%m%dT%H%M%S') 

    base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
    
    # URL parameters
    params = {
        'text': event.title,
        # Dates must be formatted as START_TIME/END_TIME
        'dates': f"{start_time}/{end_time}", 
        'details': f"{event.description}\n\nRegistered via Student Event Manager.",
        'location': event.location,
        'sf': 'true',  # Show event details page
        'output': 'xml' # Required for certain browsers/interfaces
    }

    from urllib.parse import urlencode
    return f"{base_url}&{urlencode(params)}"
