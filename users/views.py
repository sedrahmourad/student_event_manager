from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer

User = get_user_model

# Create your views here.
# registration view
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # The serializer's create method handles user creation and token generation
        user = serializer.save()

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
# login view
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
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
# profile view 
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    # Only authenticated users can access their profile
    permission_classes = (permissions.IsAuthenticated,) 
    
    # We override get_object to ensure the user can only view/edit their own profile
    def get_object(self):
        # The queryset is simply the user making the request
        return self.request.user