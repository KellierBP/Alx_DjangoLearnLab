from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Models using models.TextField() for content fields

class Post(models.Model):
    """
    Post model for social media posts.
    Users can create posts with title and content.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="Author of the post"
    )
    title = models.CharField(max_length=255, help_text="Post title")
    content = models.TextField(help_text="Post content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"{self.title} by {self.author.username}"


class Comment(models.Model):
    """
    Comment model for comments on posts.
    Users can comment on posts.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Post being commented on"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Author of the comment"
    )
    content = models.TextField(help_text="Comment content")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
