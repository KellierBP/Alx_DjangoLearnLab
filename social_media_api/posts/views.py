from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostPagination(PageNumberPagination):
    """Pagination class for posts."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentPagination(PageNumberPagination):
    """Pagination class for comments."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.
    Provides CRUD operations for posts with filtering and pagination.
    
    List: GET /api/posts/
    Create: POST /api/posts/
    Retrieve: GET /api/posts/{id}/
    Update: PUT/PATCH /api/posts/{id}/
    Delete: DELETE /api/posts/{id}/
    
    Filters: title, content (search)
    Ordering: -created_at (newest first)
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model.
    Provides CRUD operations for comments with filtering and pagination.
    
    List: GET /api/comments/
    Create: POST /api/comments/
    Retrieve: GET /api/comments/{id}/
    Update: PUT/PATCH /api/comments/{id}/
    Delete: DELETE /api/comments/{id}/
    
    Filters: post (filter by post ID)
    Ordering: -created_at (newest first)
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CommentPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Set the author to the current user when creating a comment."""
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author (if not commenting on own post)
        if comment.post.author != self.request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=comment.post
            )



class FeedView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for user feed.
    Shows posts from users that the current user follows.
    
    GET /api/feed/
    
    Returns posts ordered by creation date (newest first).
    Requires authentication.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PostPagination
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return posts from users that the current user follows.
        Ordered by creation date (newest first).
        """
        # Get the users that the current user follows
        following_users = self.request.user.following.all()
        
        # Get posts from those users, ordered by newest first
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Like
from django.contrib.contenttypes.models import ContentType


class LikePostView(APIView):
    """
    API endpoint for liking a post.
    POST: Like a post and create notification for post author.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if already liked
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response(
                {'message': 'You have already liked this post'},
                status=status.HTTP_200_OK
            )

        # Create like
        Like.objects.create(user=request.user, post=post)

        # Create notification for post author (if not liking own post)
        if post.author != request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )

        likes_count = post.likes.count()
        return Response(
            {
                'message': 'Post liked successfully',
                'likes_count': likes_count
            },
            status=status.HTTP_200_OK
        )


class UnlikePostView(APIView):
    """
    API endpoint for unliking a post.
    POST: Remove like from a post.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if liked
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            likes_count = post.likes.count()
            return Response(
                {
                    'message': 'Post unliked successfully',
                    'likes_count': likes_count
                },
                status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {'message': 'You have not liked this post'},
                status=status.HTTP_200_OK
            )
