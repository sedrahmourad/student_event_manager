# events/urls_html.py
from django.urls import path
from . import views_html

app_name = 'events_html'


urlpatterns = [
    path('events/', views_html.event_list_page, name='events_list'),
    path('events/<int:pk>/', views_html.event_detail_page, name='event_detail'),
]
