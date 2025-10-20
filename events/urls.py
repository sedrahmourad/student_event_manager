# events/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, event_list_page, event_detail_page

app_name = 'events'

router = DefaultRouter()
router.register(r'api', EventViewSet, basename='event')

urlpatterns = [
    # API routes
    path('', include(router.urls)),

    # HTML routes
    path('list/', event_list_page, name='events_list'),
    path('<int:event_id>/', event_detail_page, name='event_detail'),
]
