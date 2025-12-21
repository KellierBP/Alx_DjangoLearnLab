from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    Handles post creation, updates, and display with author information.
    """
    author = serializers.StringRelatedField(read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'author_username',
            'title',
            'content',
            'created_at',
            'updated_at',
            'comments_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        """Return the number of comments on this post."""
        return obj.comments.count()

    def create(self, validated_data):
        """Set the author to the current user."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    Handles comment creation, updates, and display with author and post information.
    """
    author = serializers.StringRelatedField(read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'post_title',
            'author',
            'author_username',
            'content',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Set the author to the current user."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
