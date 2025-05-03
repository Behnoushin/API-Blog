# -------------------   Django imports ------------------------
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# -------------------   DRF imports ------------------------
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
# -------------------   Apps imports ------------------------
from .models import Category, Post, Comment, PostLikeDislike, CommentLikeDislike, Report
from .serializers import CategorySerializer, PostSerializer, CommentSerializer, PostLikeDislikeSerializer,CommentLikeDislikeSerializer, ReportSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from utility.views import BaseAPIView

##################################################################################
#                               Category Views                                   #
##################################################################################

class CategoryListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly] 

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                "message": "دسته‌بندی با موفقیت ساخته شد ",
                "data": response.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "message": "خطایی رخ داد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class CategoryDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly] 

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response({
                "message": "دسته‌بندی با موفقیت به‌روزرسانی شد ",
                "data": response.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "message": "به‌روزرسانی انجام نشد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                "message": "دسته‌بندی با موفقیت حذف شد "
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response({
                "message": "حذف انجام نشد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

##################################################################################
#                                Posts Views                                     #
##################################################################################

class PostListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                "message": "پست با موفقیت ساخته شد ",
                "data": response.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "message": "خطایی در ساخت پست رخ داد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response({
                "message": "پست با موفقیت به روزرسانی شد ",
                "data": response.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "message": "خطایی در به روزرسانی پست رخ داد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        try:
            post = self.get_object()
            post.delete()
            return Response({
                "message": "پست با موفقیت حذف شد "
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response({
                "message": "خطایی در حذف پست رخ داد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


##################################################################################
#                                Comments Views                                  #
##################################################################################

class CommentListCreateView(BaseAPIView, generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                "message": "کامنت با موفقیت ثبت شد ",
                "data": response.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "message": "ثبت کامنت انجام نشد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return Response({
                "message": "کامنت با موفقیت به‌روزرسانی شد ",
                "data": response.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "message": "به‌روزرسانی کامنت انجام نشد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
            comment.delete()
            return Response({
                "message": "کامنت با موفقیت حذف شد "
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response({
                "message": "حذف کامنت انجام نشد. لطفاً دوباره تلاش کنید.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


##################################################################################
#                         Post Like/Dislike Views                                #
##################################################################################

class PostLikeDislikeView(BaseAPIView, generics.GenericAPIView):
    serializer_class = PostLikeDislikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        is_like = request.data.get("is_like")

        if is_like is None:
            return Response({"error": "فیلد is_like الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        obj, created = PostLikeDislike.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={"is_like": is_like}
        )

        serializer = self.get_serializer(obj)
        message = "رای ثبت شد " if created else "رای به‌روزرسانی شد "

        return Response({
            "message": message,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
##################################################################################
#                         Comment Like/Dislike Views                             #
##################################################################################

class CommentLikeDislikeView(generics.GenericAPIView):
    serializer_class = CommentLikeDislikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_id)
        is_like = request.data.get("is_like")

        if is_like is None:
            return Response({"error": "فیلد is_like الزامی است."}, status=status.HTTP_400_BAD_REQUEST)

        obj, created = CommentLikeDislike.objects.update_or_create(
            user=request.user,
            comment=comment,
            defaults={"is_like": is_like}
        )

        serializer = self.get_serializer(obj)
        message = "رای ثبت شد " if created else "رای به‌روزرسانی شد "

        return Response({
            "message": message,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
   

##################################################################################
#                                Report Views                                    #
##################################################################################

class ReportView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Report.objects.get(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": " گزارش شما با موفقیت ارسال شد."
                }, status=status.HTTP_201_CREATED)
        
        else:
            return Response({
                "message": " خطا پیش آمده، لطفاً مجدداً بررسی کنید.", 
                "errors": serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
