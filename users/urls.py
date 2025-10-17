from django.urls import path
from django.contrib.auth import views as auth_views 
# Import both the API classes AND the frontend view functions
from .views import (
    RegisterView, LoginView, ProfileView,
    register_page, login_page, user_dashboard, logout_view
)

urlpatterns = [
    # --- FRONTEND/HTML ROUTES ---
    # GET /users/register/ (Renders the registration form)
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    #path('', register_page, name='register'),
    
    # GET /users/login/ (Renders the login form)
    path('', login_page, name='login'),
    
    # GET /users/dashboard/ (Renders the dashboard page)
    path('dashboard/', user_dashboard, name='dashboard'),
    
    # GET /users/logout/ (Logs the user out and redirects)
    path('logout/', logout_view, name='logout'),

    # --- API ROUTES (Django REST Framework) ---
    # POST /api/users/register/ (Handles registration data)
    path('register/', RegisterView.as_view(), name='api_register'),
    
    # POST /api/users/login/ (Handles login credentials)
    #path('login/', LoginView.as_view(), name='api_login'),
    
    # GET/PUT /api/users/profile/ (Handles profile data)
    path('api/profile/', ProfileView.as_view(), name='api_profile'),
]