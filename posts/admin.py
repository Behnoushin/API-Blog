from django.contrib import admin
from .models import Category, Post, Comment, LikeDislike, Report

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
    
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'reaction']
    search_fields = ['user__username', 'post__title', 'comment__content']
    ordering = ['-reaction']  
    list_filter = ['reaction', 'user', 'post', 'comment']
    readonly_fields = ['created_at', 'updated_at']
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
admin.site.register(LikeDislike, LikeDislikeAdmin)
admin.site.register(Report, ReportAdmin)
