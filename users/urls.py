from django.urls import path
from .views import RegisterView, LoginView, ProfileView

urlpatterns = [
    # POST /api/users/register/ [cite: 16]
    path('register/', RegisterView.as_view(), name='register'),
    
    # POST /api/users/login/ [cite: 24]
    path('login/', LoginView.as_view(), name='login'),
    
    # GET/PUT /api/users/profile/ [cite: 26, 28]
    path('profile/', ProfileView.as_view(), name='profile'),
]