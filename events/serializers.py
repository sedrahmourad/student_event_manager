from rest_framework import serializers
from .models import Event, Comment, Like
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    # displays the name of the user who commented 
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_name', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']
# main event serializer
class EventSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    organizer_name = serializers.CharField(source='organizer.name', read_only=True)
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location', 'date', 
            'category', 
            # We need 'organizer' here so the ViewSet can set it
            'organizer', 'organizer_name', 
            'likes_count', 'comments', 'is_liked'
        ]
        # ONLY calculated fields are read-only.
        # 'organizer' must be writable here so the view can set it.
        read_only_fields = ['organizer_name', 'likes_count', 'is_liked']
        
        # We explicitly set 'organizer' to not be required for the client 
        # (as the view sets it)
        extra_kwargs = {
            'organizer': {'required': False, 'allow_null': True}
        }
    def get_likes_count(self, obj):
        return obj.likes.count()
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False