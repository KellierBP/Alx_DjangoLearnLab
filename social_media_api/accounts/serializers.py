from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles password validation and user creation with token generation.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'bio', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """Create user and generate authentication token."""
        validated_data.pop('password2')
        # Use get_user_model().objects.create_user for creating the user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # Create token for the user
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates credentials and returns user data with token.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile display and updates.
    Shows user information including followers count.
    """
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'bio',
            'profile_picture',
            'followers_count',
            'following_count',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_followers_count(self, obj):
        """Return the number of followers."""
        return obj.followers.count()

    def get_following_count(self, obj):
        """Return the number of users this user is following."""
        return obj.following.count()
