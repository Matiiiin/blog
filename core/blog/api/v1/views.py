from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from blog.models import Post, Image, Category, Comment, CommentReply
from .serializers import (
    PostModelSerializer,
    ImageModelSerializer,
    CategoryModelSerializer,
    CommentModelSerializer,
    CommentReplyModelSerializer,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)
from .permissions import IsVerifiedUser, IsOwner
from .paginations import PostPagination
from rest_framework.mixins import ListModelMixin, CreateModelMixin
import logging

logger = logging.getLogger(__name__)

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
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_fields = [
        "title",
        "main_content",
        "author__first_name",
        "author__last_name",
    ]
    search_fields = ["title", "main_content"]
    ordering_fields = ["title", "created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVerifiedUser()]


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    A class for retrieving, updating and deleting posts.
    """

    serializer_class = PostModelSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVerifiedUser(), IsOwner()]


class ImageGenericViewSet(viewsets.GenericViewSet):
    serializer_class = ImageModelSerializer
    queryset = Image.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        if self.request.method in ["PUT", "DELETE"]:
            return [
                IsAuthenticated(),
                IsVerifiedUser(),
                IsAdminUser(),
            ]
        return [IsAuthenticated(), IsVerifiedUser()]

    def list(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, pk=None):
        try:
            image = self.get_object()
            serializer = self.get_serializer(image)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, pk=None):
        try:
            image = self.get_object()
            serializer = self.get_serializer(image, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(e)
            return Response(
                {"details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, pk=None):
        try:
            image = self.get_object()
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response(
                {"details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CategoryModelViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUser(), IsVerifiedUser()]


class CommentModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentModelSerializer
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated(), IsVerifiedUser()]
        return [IsAuthenticated(), IsVerifiedUser(), IsOwner()]


class CommentReplyModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentReplyModelSerializer
    queryset = CommentReply.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated(), IsVerifiedUser()]
        return [IsAuthenticated(), IsVerifiedUser(), IsOwner()]
