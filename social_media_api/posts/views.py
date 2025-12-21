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
        serializer.save(author=self.request.user)
