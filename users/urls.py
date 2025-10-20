from django.urls import path
from django.contrib.auth import views as auth_views 
# Import both the API classes AND the frontend view functions
from . import views
from .views import RegisterView, LoginView, ProfileView

app_name = "users"

urlpatterns = [
    path("register/", views.register_page, name="register_page"), # root will show register page
    path("login/", views.login_page, name="login_page"),
    path("dashboard/", views.user_dashboard, name="dashboard_page"),

    # API Views (JSON Endpoints for your front-end or Postman)
    path("/register/", RegisterView.as_view(), name="register_api"),
    path("/login/", LoginView.as_view(), name="login_api"),
    path("/profile/", ProfileView.as_view(), name="profile_api"),
]