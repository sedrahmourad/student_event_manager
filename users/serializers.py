from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

User = get_user_model

# registration serializer 
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User 
        fields = ('id', 'role', 'name', 'email', 'password', 'major', 'organization_name')
        read_only_fields = ('id',)
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True}
        }
    # Custom validation for role-specific fields
    def validate(self, data):
        role = data.get('role')
        major = data.get('major')
        organization_name = data.get('organization_name')

        if role == 'student':
            # Student requires 'major' and cannot have 'organization_name' 
            if not major:
                raise serializers.ValidationError({"major": "Students must specify a major."})
            if organization_name:
                raise serializers.ValidationError({"organization_name": "Students cannot have an organization name."})
            data['organization_name'] = None # Ensure it's null/empty

        elif role == 'organizer':
            # Organizer requires 'organization_name' and cannot have 'major'
            if not organization_name:
                raise serializers.ValidationError({"organization_name": "Organizers must specify an organization name."})
            if major:
                raise serializers.ValidationError({"major": "Organizers cannot have a major."})
            data['major'] = None # Ensure it's null/empty
        
        else:
            raise serializers.ValidationError({"role": "Role must be 'student' or 'organizer'."})

        return data
    
    def create(self, validated_data):
        # The user's username is inherited from AbstractUser. 
        # For simplicity, we will use the email as the username if not provided,

        password = validated_data.pop('password')
        
        # Use create_user to ensure the password is correctly hashed
        user = get_user_model().objects.create_user(
            username=validated_data.get('email'), # Use email as a unique identifier for username
            email=validated_data.get('email'),
            password=password,
            **validated_data
        )

        # Create the authentication token immediately for login after registration
        Token.objects.create(user=user)

        return user
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials.", code='authorization')
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        
        data['user'] = user
        return data 
    
# profile serializer
class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('id', 'role', 'name', 'email', 'major', 'organization_name')
        # Only the 'major' and 'organization_name' fields can be updated
        read_only_fields = ('id', 'role', 'email')
    def validate(self, data):
        user = self.instance
        # Enforce role-specific field validation during update
        if user.role == 'student':
            if 'organization_name' in data:
                raise serializers.ValidationError({"organization_name": "Students cannot set organization name."})
        elif user.role == 'organizer':
            if 'major' in data:
                raise serializers.ValidationError({"major": "Organizers cannot set a major."})

        return data