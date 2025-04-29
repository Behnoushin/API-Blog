from rest_framework import serializers
from utility.serializers import BaseSerializer
from .models import CustomUser, UserProfile

##################################################################################
#                           UserProfile serializers                              #
##################################################################################

class UserProfileSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = UserProfile
        fields = "__all__"

##################################################################################
#                           UserProfile serializers                              #
##################################################################################

class UserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = CustomUser
        fields = "__all__"

##################################################################################
#                           UserProfile serializers                              #
##################################################################################
     
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    
##################################################################################
#                           UserProfile serializers                              #
##################################################################################

class EmailSerializer(BaseSerializer):
    email = serializers.EmailField()
    class Meta:
        model = CustomUser
        fields = ['email']