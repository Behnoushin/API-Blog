from django.contrib import admin
from .models import Category, Post, Comment, PostLikeDislike, CommentLikeDislike, Report

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    search_fields = ['title', 'content', 'author__username']
    ordering = ['-created_at']
    list_filter = ['created_at', 'author']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    ordering = ['-created_at']
    list_filter = ['created_at', 'author', 'post']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
class PostLikeDislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'is_like']
    search_fields = ['user__username', 'post__title']
    list_filter = ['is_like', 'user', 'post']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-is_like']
    list_per_page = 20

class CommentLikeDislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'is_like']
    search_fields = ['user__username', 'comment__content']
    list_filter = ['is_like', 'user', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-is_like']
    list_per_page = 20

    
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'comment', 'reason', 'created_at']
    search_fields = ['user__username', 'post__title', 'comment__content', 'reason']
    ordering = ['-created_at']
    list_filter = ['reason', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostLikeDislike, PostLikeDislikeAdmin)
admin.site.register(CommentLikeDislike, CommentLikeDislikeAdmin)
admin.site.register(Report, ReportAdmin)
