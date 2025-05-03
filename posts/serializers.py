from rest_framework import serializers
from .models import Category, Post, Comment, PostLikeDislike, CommentLikeDislike, Report
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
#                        Post Like/Diskike serializers                           #
##################################################################################

class PostLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikeDislike
        fields = "__all__"
 
##################################################################################
#                      Comment Like/Diskike serializers                          #
##################################################################################       

class CommentLikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLikeDislike
        fields = "__all__"

        
##################################################################################
#                           Report serializers                                   #
##################################################################################

class ReportSerializer(BaseSerializer):
    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = ['id', 'user']
