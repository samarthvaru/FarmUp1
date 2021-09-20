from rest_framework import serializers

from post.models import Post
from api.comment.serializers import CommentSerializer


class PostListSerializer(serializers.ModelSerializer):
    """DRF Serializer Listing All The Blog Posts"""

    total_comments = serializers.IntegerField()


    class Meta:
        model = Post
        fields = ['slug', 'title', 'short_description',
                  'total_comments', 'author', 'published_on']


class PostDetailSerializer(serializers.ModelSerializer):
    """DRF Serializer For Details Of The Blog Posts"""

    comments_list = CommentSerializer(many=True)
    total_comments = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ['slug', 'title', 'body', 'author',
                  'published_on', 'comments_list', 'short_description', 'total_comments']


class PostAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['slug', 'title', 'body', 'author',
                  'published_on', 'short_description' ]