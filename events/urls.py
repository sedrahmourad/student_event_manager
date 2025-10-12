# events/urls.py

from rest_framework.routers import DefaultRouter
from .views import EventViewSet

router = DefaultRouter()
# This single line creates all 7 RESTful routes (list, create, retrieve, update, delete)
router.register(r'', EventViewSet, basename='event')

urlpatterns = router.urls