from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=True)
    password = serializers.CharField(source='user.password', write_only=True)
    email = serializers.CharField(source='user.email', required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'password', 'email', 'friends']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            email=user_data.get('email', '')
        )
        
        profile = UserProfile.objects.create(user=user)
        return profile