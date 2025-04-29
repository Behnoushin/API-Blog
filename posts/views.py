# -------------------   DRF imports ------------------------
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
# -------------------   Apps imports ------------------------
from .models import Category, Post, Comment, LikeDislike, Report
from .serializers import CategorySerializer, PostSerializer, CommentSerializer, LikeDislikeSerializer, ReportSerializer
from utility.views import BaseAPIView


##################################################################################
#                               Category Views                                   #
##################################################################################

class CategoryListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    def get_categories(self, request):
        """Get a list of categories."""
        categories = self.get_queryset()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create_category(self, request):
        """Create a new category. (Only admin users can create.)"""
        if not request.user.is_staff:
            return Response({"message": "فقط مدیران سایت می‌توانند دسته‌بندی جدید بسازند."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "دسته‌بندی جدید با موفقیت ساخته شد."}, status=status.HTTP_201_CREATED)
        
        return Response({"message": "ساخت دسته‌بندی ناموفق بود. لطفاً داده‌ها را بررسی کنید."}, status=status.HTTP_400_BAD_REQUEST)
        
        
class CategoryDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    def get_category(self, request, pk):
        """Retrieve a specific category."""
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update_category(self, request, pk):
        """Update a category (only for admins)."""
        if not request.user.is_staff:
            return Response({"message": "فقط مدیران سایت می‌توانند دسته‌بندی را بروزرسانی کنند."}, status=status.HTTP_403_FORBIDDEN)

        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "دسته‌بندی با موفقیت بروزرسانی شد."}, status=status.HTTP_200_OK)
        
        return Response({"message": "بروزرسانی دسته‌بندی ناموفق بود. لطفاً داده‌ها را بررسی کنید."}, status=status.HTTP_400_BAD_REQUEST)


    def delete_category(self, request, pk):
        """Delete a category (only for admins)."""
        if not request.user.is_staff:
            return Response({"message": "فقط مدیران سایت می‌توانند دسته‌بندی را حذف کنند."}, status=status.HTTP_403_FORBIDDEN)
        
        category = self.get_object()
        category.delete()
        return Response({"message": "دسته‌بندی با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)



##################################################################################
#                                Posts Views                                     #
##################################################################################

class PostListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_posts(self, request):
        """Get a list of posts."""
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create_post(self, request):
        """Create a new post."""
        if not request.user.is_authenticated or request.user.is_staff:
            return Response({"message": "برای ایجاد پست باید وارد حساب کاربری خود شوید."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user) 
            return Response({"message": "پست جدید با موفقیت ایجاد شد."}, status=status.HTTP_201_CREATED)
        
        return Response({"message": "ایجاد پست ناموفق بود. لطفاً داده‌ها را بررسی کنید."}, status=status.HTTP_400_BAD_REQUEST)
    
    
class PostDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    
    def get_post(self, request, pk):
        """Retrieve a specific post."""
        post = self.get_object()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def update_post(self, request, pk):
        """Update a post (only for the post's author)."""
        if not request.user.is_authenticated:
            return Response({"message": "برای بروزرسانی پست باید وارد حساب کاربری خود شوید."}, status=status.HTTP_401_UNAUTHORIZED)

        post = self.get_object()
        if post.author != request.user:
            return Response({"message": "شما مجاز به بروزرسانی پست دیگران نیستید."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "پست با موفقیت بروزرسانی شد."}, status=status.HTTP_200_OK)
        
        return Response({"message": "بروزرسانی پست ناموفق بود. لطفاً داده‌ها را بررسی کنید."}, status=status.HTTP_400_BAD_REQUEST)


    def delete_post(self, request, pk):
        """Delete a post (only for the post's author)."""
        if not request.user.is_authenticated:
            return Response({"message": "برای حذف پست باید وارد حساب کاربری خود شوید."}, status=status.HTTP_401_UNAUTHORIZED)

        post = self.get_object()
        if post.author != request.user:
            return Response({"message": "شما مجاز به حذف پست دیگران نیستید."}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"message": "پست با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)
    
    
##################################################################################
#                                Comments Views                                  #
##################################################################################

class CommentListCreateView(BaseAPIView, generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_comment(self, request):
        """Get a list of comments."""
        comments = self.get_queryset()
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create_comment(self, request):
        """Create a new comment."""
        if not request.user.is_authenticated or request.user.is_staff:
            return Response({"message": "برای ثبت کامنت باید وارد حساب کاربری خود شوید."}, status=status.HTTP_401_UNAUTHORIZED)  
             
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"message": "کامنت شما ثبت شد."}, status=status.HTTP_201_CREATED)
        
        return Response({"message": "کامنت شما ثبت نشد. لطفاً داده‌ها را بررسی کنید."}, status=status.HTTP_400_BAD_REQUEST)  
 

class CommentDetailView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_comment(self, request, *args, **kwargs):
        """Get a specific comment."""
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    
    def update_comment(self, request, *args, **kwargs):
        """Update an existing comment."""
        comment = self.get_object()

        if comment.user != request.user:
            return Response({"message": "شما نمی‌توانید کامنت دیگران را تغییر دهید."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کامنت شما با موفقیت به‌روزرسانی شد."}, status=status.HTTP_200_OK)
        
        return Response({"message": "به‌روزرسانی کامنت با مشکل مواجه شد."}, status=status.HTTP_400_BAD_REQUEST)


    def delete_comment(self, request, *args, **kwargs):
        """Delete a comment."""
        comment = self.get_object()
        
        if comment.user != request.user:
            return Response({"message": "شما نمی‌توانید کامنت دیگران را حذف کنید."}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response({"message": "کامنت شما با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)


##################################################################################
#                         Like and Dislike Views                                 #
##################################################################################

class PostLikeDislikeView(BaseAPIView, generics.ListCreateAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer

    def get_like_dislike(self, request, post_id):
        """Get a list of likes and dislikes for a specific post."""
        post = Post.objects.get(id=post_id)
        likes_dislikes = LikeDislike.objects.filter(post=post)
        serializer = self.get_serializer(likes_dislikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_like_dislike(self, request, post_id):
        """Create a new like or dislike on a post."""
        if not request.user.is_authenticated or request.user.is_staff:
            return Response({"message": "برای ثبت لایک یا دیسلایک باید وارد حساب کاربری خود شوید."}, status=status.HTTP_401_UNAUTHORIZED)

        post = Post.objects.get(id=post_id)
        reaction = request.data.get('reaction')
        if reaction not in ['like', 'dislike']:
            return Response({"message": "لطفاً انتخاب صحیح انجام دهید: 'like' یا 'dislike'."}, status=status.HTTP_400_BAD_REQUEST)

        like_dislike, created = LikeDislike.objects.update_or_create(user=request.user, post=post, defaults={'reaction': reaction})
        if created:
            return Response({"message": f"پست با موفقیت {reaction} شد."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"پست شما به {reaction} تغییر یافت."}, status=status.HTTP_200_OK)


    def delete_like_dislike(self, request, post_id):
        """Delete a like or dislike from a post."""
        if not request.user.is_authenticated or request.user.is_staff:
            return Response({"message": "برای حذف لایک یا دیسلایک باید وارد حساب کاربری خود شوید."}, status=status.HTTP_401_UNAUTHORIZED)

        post = Post.objects.get(id=post_id)

        try:
            like_dislike = LikeDislike.objects.get(user=request.user, post=post)
        except LikeDislike.DoesNotExist:
            return Response({"message": "شما هیچ لایک یا دیسلایکی برای این پست ثبت نکرده‌اید."},
                            status=status.HTTP_404_NOT_FOUND)

        like_dislike.delete()
        return Response({"message": "لایک یا دیسلایک شما با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)


class CommentLikeDislikeView(BaseAPIView, generics.ListCreateAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer

    def get_like_dislike(self, request, comment_id):
        """Get a list of likes and dislikes for a specific comment."""
        comment = Comment.objects.get(id=comment_id)
        likes_dislikes = LikeDislike.objects.filter(comment=comment)
        serializer = self.get_serializer(likes_dislikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create_like_dislike(self, request, comment_id):
        """Create a new like or dislike on a comment."""
        if not request.user.is_authenticated or request.user.is_staff:
            return Response({"message": "برای ثبت لایک یا دیسلایک باید وارد حساب کاربری خود شوید."}, status=status.HTTP_401_UNAUTHORIZED)

        comment = Comment.objects.get(id=comment_id)
        reaction = request.data.get('reaction')

        if reaction not in ['like', 'dislike']:
            return Response({"message": "لطفاً انتخاب صحیح انجام دهید: 'like' یا 'dislike'."}, status=status.HTTP_400_BAD_REQUEST)

        like_dislike, created = LikeDislike.objects.update_or_create(user=request.user, comment=comment, defaults={'reaction': reaction})

        if created:
            return Response({"message": f"کامنت با موفقیت {reaction} شد."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"کامنت شما به {reaction} تغییر یافت."}, status=status.HTTP_200_OK)


    def delete_like_dislike(self, request, comment_id):
        """Delete a like or dislike from a comment."""
        if not request.user.is_authenticated or request.user.is_staff:
            return Response({"message": "برای حذف لایک یا دیسلایک باید وارد حساب کاربری خود شوید."}, status=status.HTTP_401_UNAUTHORIZED)

        comment = Comment.objects.get(id=comment_id)

        try:
            like_dislike = LikeDislike.objects.get(user=request.user, comment=comment)
        except LikeDislike.DoesNotExist:
            return Response({"message": "شما هیچ لایک یا دیسلایکی برای این کامنت ثبت نکرده‌اید."}, status=status.HTTP_404_NOT_FOUND)

        like_dislike.delete()
        return Response({"message": "لایک یا دیسلایک شما با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)

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
            return Response({"message": " گزارش شما با موفقیت ارسال شد."}, status=status.HTTP_201_CREATED)
        
        else:
            return Response({"message": " خطا پیش آمده، لطفاً مجدداً بررسی کنید.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
