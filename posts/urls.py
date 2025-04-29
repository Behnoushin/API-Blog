from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView,
    PostLikeDislikeView, CommentLikeDislikeView,
    ReportView
)

urlpatterns = [
    # -------------------------------- Category URLs -----------------------------------
    path("categories/", CategoryListCreateView.as_view(), name='category-list-create'),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name='category-detail'),
    
    # -------------------------------- Posts URLs ---------------------------------------
    path("posts/", PostListCreateView.as_view(), name='post-list-create'),
    path("posts/<int:pk>/", PostDetailView.as_view(), name='post-detail'),
    
    # -------------------------------- Comments URLs -------------------------------------
    path("comments/", CommentListCreateView.as_view(), name='comment-list-create'),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name='comment-detail'),
    
    # ----------------------- Post Like/Dislike URLs --------------------------------------
    path('post/<int:post_id>/like-dislike/', PostLikeDislikeView.as_view(), name='post-like-dislike'),
    path('post/<int:post_id>/like-dislike/delete/', PostLikeDislikeView.as_view(), name='delete-post-like-dislike'),
    
    # ----------------------- Comment Like/Dislike URLs ------------------------------------
    path('comment/<int:comment_id>/like-dislike/', CommentLikeDislikeView.as_view(), name='comment-like-dislike'),
    path('comment/<int:comment_id>/like-dislike/delete/', CommentLikeDislikeView.as_view(), name='delete-comment-like-dislike'),
    
    # -------------------------------- Reports URLs ----------------------------------------
    path('reports/', ReportView.as_view(), name='report-list-create'),

]