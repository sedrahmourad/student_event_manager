from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Assuming these serializers are defined in users/serializers.py
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

User = get_user_model() # Correct way to call the custom user model function

# --- 1. FRONTEND VIEWS (For rendering HTML pages) ---

def register_page(request):
    """Renders the registration form page (users/register.html)."""
    return render(request, 'users/register.html')

def login_page(request):
    """Renders the login form page (users/login.html)."""
    return render(request, 'users/login.html')

@login_required
def user_dashboard(request):
    """Renders the user's dashboard (users/dashboard.html)."""
    # Note: The 'user' object is automatically passed to the template by the login_required decorator.
    return render(request, 'users/dashboard.html')

def logout_view(request):
    """Logs the user out and redirects to the login page."""
    logout(request)
    return redirect('users:login')


# --- 2. API VIEWS (For handling JSON data requests) ---

class RegisterView(generics.CreateAPIView):
    """
    POST /api/users/register/
    Handles user registration and returns a token upon success.
    """
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # The serializer's create method handles user creation
        user = serializer.save()

        # Generate or retrieve the authentication token
        token, created = Token.objects.get_or_create(user=user)

        # Return the token and essential user details 
        response_data = {
            'token': token.key,
            'user': {
                'id': user.pk,
                'email': user.email,
                'role': user.role,
                'name': user.name,
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    """
    POST /api/users/login/
    Authenticates user credentials and returns a token.
    """
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Generate or retrieve the authentication token
        token, created = Token.objects.get_or_create(user=user)
        
        response_data = {
            'token': token.key,
            'user': {
                'id': user.pk,
                'email': user.email,
                'role': user.role,
                'name': user.name,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/users/profile/ - Retrieve user's profile details.
    PUT/PATCH /api/users/profile/ - Update user's profile details.
    """
    serializer_class = ProfileSerializer
    # Only authenticated users can access their profile
    permission_classes = (permissions.IsAuthenticated,) 
    
    # We override get_object to ensure the user can only view/edit their own profile
    def get_object(self):
        """Returns the user instance associated with the current request."""
        return self.request.user
