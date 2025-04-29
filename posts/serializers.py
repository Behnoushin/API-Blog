from rest_framework import serializers
from .models import Category, Post, Comment, LikeDislike, Report
from utility.serializers import BaseSerializer

##################################################################################
#                           Category serializers                                 #
##################################################################################

class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
##################################################################################
#                           Post serializers                                     #
##################################################################################

class PostSerializer(BaseSerializer):
    class Meta:
        model = Post
        fields = "__all__"

##################################################################################
#                           Comment serializers                                  #
##################################################################################
      
class CommentSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

##################################################################################
#                           Like/Dislike serializers                             #
##################################################################################

class LikeDislikeSerializer(BaseSerializer):
    class Meta:
        model = LikeDislike
        fields = "__all__"
        
##################################################################################
#                           Report serializers                                   #
##################################################################################

class ReportSerializer(BaseSerializer):
    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = ['id', 'user']
