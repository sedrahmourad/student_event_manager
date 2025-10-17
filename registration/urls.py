from django.urls import path
from .views import RegistrationListCreateView, RegistrationCancelView

# Define the namespace for this app's URLs
app_name = 'registration'

urlpatterns = [
    # POST /api/registrations/ - Register for an event
    # GET /api/registrations/ - View all registered events for the current student
    path('', RegistrationListCreateView.as_view(), name='registration-list-create'),
    
    # DELETE /api/registrations/{id}/cancel/ - Cancel a specific registration
    path('<int:pk>/cancel/', RegistrationCancelView.as_view(), name='registration-cancel'),
]
