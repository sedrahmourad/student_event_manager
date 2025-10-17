from django.apps import AppConfig


class RegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registration'
    # Optional: A human-readable name for the app (useful in the Admin)
    verbose_name = '3. Registrations'
    # method called by django when the app is loaded
    def ready(self):
        """
        Loads the signal handlers to ensure they are connected 
        to the database events (like model creation).
        """
        # We import the signals file here to connect the @receiver decorators
        # to their respective signals (e.g., post_save on Registration model).
        import registration.signals 


