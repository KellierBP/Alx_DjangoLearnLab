from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    POST: Create a new user account and return authentication token.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API endpoint for user login.
    POST: Authenticate user and return authentication token.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile.
    GET: Retrieve authenticated user's profile.
    PUT/PATCH: Update authenticated user's profile.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the authenticated user."""
        return self.request.user


class FollowView(APIView):
    """
    API endpoint for following a user.
    POST: Add a user to the current user's following list.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent self-follow
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already following
        if request.user.following.filter(id=user_id).exists():
            return Response(
                {'message': 'You are already following this user'},
                status=status.HTTP_200_OK
            )

        # Add to following list
        request.user.following.add(user_to_follow)
        
        return Response(
            {
                'message': f'You are now following {user_to_follow.username}',
                'user': UserSerializer(user_to_follow).data
            },
            status=status.HTTP_200_OK
        )


class UnfollowView(APIView):
    """
    API endpoint for unfollowing a user.
    POST: Remove a user from the current user's following list.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if currently following
        if not request.user.following.filter(id=user_id).exists():
            return Response(
                {'message': 'You are not following this user'},
                status=status.HTTP_200_OK
            )

        # Remove from following list
        request.user.following.remove(user_to_unfollow)
        
        return Response(
            {
                'message': f'You have unfollowed {user_to_unfollow.username}',
                'user': UserSerializer(user_to_unfollow).data
            },
            status=status.HTTP_200_OK
        )
