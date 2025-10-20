from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model, login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from datetime import date, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Assuming these serializers are defined in users/serializers.py
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

User = get_user_model() # Correct way to call the custom user model function

# --- 1. FRONTEND VIEWS (For rendering HTML pages) ---

def register_page(request):
    """Renders the registration form page (users/registration.html)."""
    print("Rendering registration page...") # to check where the system fails
     # DEBUG: Check if URL reversing works
    print("Reversed login URL:", reverse("users:login_page"))
    return render(request, 'users/registration.html')

def login_page(request):
    print("rendering login page...")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("users:dashboard")
        else:
            return render(request, "users/login.html", {"error": "Invalid email or password"})

    return render(request, "users/login.html")

@login_required
def user_dashboard(request):
    """Renders the user's dashboard (users/dashboard.html)."""
    current_user = request.user
    context = {
        'user': current_user,
        'registered_events': [],
        'created_events': [],
    }

    # --- MOCK DATA FOR TESTING THE TEMPLATE ---
    # NOTE: In a real app, replace this block with database queries 
    # (e.g., Registration.objects.filter(user=current_user))
    
    if current_user.role == 'student':
        # Mock registered events for student role
        context['registered_events'] = [
            {'id': 1, 'event': {'id': 101, 'title': 'Hackathon 2025', 'date': date.today() + timedelta(days=15), 'category': 'Tech'}, 'registration_id': 501},
            {'id': 2, 'event': {'id': 102, 'title': 'Business Case Competition', 'date': date.today() + timedelta(days=30), 'category': 'Business'}, 'registration_id': 502},
        ]
        
    elif current_user.role == 'organizer':
        # Mock created events for organizer role
        context['created_events'] = [
            {'id': 201, 'title': 'Robotics Exhibition', 'date': date.today() + timedelta(days=20), 'attendee_count': 45, 'status': 'Active'},
            {'id': 202, 'title': 'Finance Career Fair', 'date': date.today() + timedelta(days=60), 'attendee_count': 120, 'status': 'Pending'},
        ]
    # --- END MOCK DATA ---
    
    # You must also define the user's name, role, major/organization_name in your CustomUser model
    # and ensure they are populated here. (This is generally handled by the request.user object itself)
    
    return render(request, 'users/dashboard.html', context)

def logout_view(request):
    """Logs the user out and redirects to the login page."""
    logout(request)
    return redirect('users:login_page')


# --- 2. API VIEWS (For handling JSON data requests) ---
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        print("✅ RegisterView reached!")  # Debug line
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
            }
        }, status=status.HTTP_201_CREATED)

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
        # FIX ADDED HERE: Establish the Django session.
        # This sends the session cookie back to the browser, satisfying @login_required.
        login(request, user) 
        
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