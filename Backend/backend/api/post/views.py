from rest_framework import generics 
from rest_framework.permissions import AllowAny
from .serializers import PostListSerializer, PostDetailSerializer,PostAddSerializer
from post.models import Post

class PostListView(generics.ListAPIView):
    """View For List All Published Posts"""
    permission_classes=[AllowAny]
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostListSerializer
    lookup_field = 'slug'


class PostDetailView(generics.RetrieveAPIView):
    """View For The Details Of A Single Post"""
    permission_classes=[AllowAny]
    queryset = Post.objects.all()   
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

class PostAdd(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=PostAddSerializer


