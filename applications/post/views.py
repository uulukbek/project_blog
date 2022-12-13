from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from applications.post.models import Post, Category, Comment
from applications.post.serializers import *
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.permissions import *
from applications.post.permissions import IsOwner, IsCommentOwner
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination

# class PostAPIView(ViewSet):
#     def list(self, request):
#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=HTTP_201_CREATED)
        

#*Пагинация
class LargeResultSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_parm = 'page_size'
    max_page_size = 10000

#* Способ 2 - ModelViewSet        
class PostAPIView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner]
    pagination_class = LargeResultSetPagination
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'owner']
    search_fields = ['title', 'description']
    ordering_fields = ['id']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk, *args, **kwargs):  #post/id/like
        like_obj, _ = Like.objects.get_or_create(post_id=pk, owner=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return  Response({'status' : status})

    @action(detail=True, methods=['POST'])
    def rating(self,request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(post_id=pk, owner=request.user)
        rating_obj.rating = request.data['rating']
        rating_obj.save()
        return Response({'status' : status.HTTP_201_CREATED})


    # def get_queryset(self):
    #     queriset = super().get_queryset()
    #     filter_ = self.request.query_params.get('category')
    #     if filter_:
    #         queriset = queriset.filter(category=filter_)
    #     return queriset[0:3]

class CategoryAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentAPIView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queriset = super().get_queryset()
        queriset = queriset.filter(owner=self.request.user)
        return queriset