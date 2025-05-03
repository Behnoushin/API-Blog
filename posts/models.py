from django.db import models
from utility.models import BaseModel
from users.models import CustomUser

##################################################################################
#                           Category Model                                       #
##################################################################################

class Category(BaseModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
 
##################################################################################
#                           Post Model                                           #
##################################################################################   
    
class Post(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='posts')
    
    class Meta:
        ordering = ("-created_at",)
        
    def __str__(self):
        return f"{self.title} by {self.author.username}"
 
##################################################################################
#                           Comment Model                                        #
##################################################################################   
    
class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    
    def __str__(self):
        return f"comment by {self.author.username} on {self.post.title}"

##################################################################################
#                          Post Like/Diskike Model                               #
##################################################################################

class PostLikeDislike(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_dislikes')
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.is_like else 'Dislike'} - Post: {self.post.id}"


##################################################################################
#                         Comment Like/Diskike Model                             #
##################################################################################

class CommentLikeDislike(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes_dislikes')
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.is_like else 'Dislike'} - Comment: {self.comment.id}"

    
##################################################################################
#                           Report Model                                         #
##################################################################################
   
class Report(BaseModel):
    REPORT_CHOICES = [
        ('ABUSE', 'Abuse'),
        ('OTHER', 'Other'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_CHOICES)
    message = models.TextField(blank=True)