from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from blog.models import Post
from .serializers import PostModelSerializer
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from .permissions import IsVerifiedUser , IsPostOwner
from .paginations import PostPagination

# class PostModelViewSet(viewsets.ModelViewSet):
#     serializer_class = PostModelSerializer
#     queryset = Post.objects.all()
#     permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['title', 'content']
    # search_fields = ['title', 'content']
    # ordering_fields = ['title', 'created_at']
    # def list(self, request, *args, **kwargs):

class PostListCreateAPIView(ListCreateAPIView):
    """
    A class for creating and listing posts, utilizing features like search, ordering and filtering.
    """
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'main_content' , 'author__first_name' , 'author__last_name']
    search_fields = ['title', 'main_content']
    ordering_fields = ['title', 'created_at']
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVerifiedUser()]

class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    A class for retrieving, updating and deleting posts.
    """
    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVerifiedUser(), IsPostOwner()]