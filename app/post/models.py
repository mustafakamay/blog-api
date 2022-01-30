from django.db import models
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

class Post(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,related_name="posts_user")
    title = models.CharField(max_length=50,null=False,blank=False)
    content = models.TextField(max_length=200,null=False,blank=False)
    favorited_by = models.ManyToManyField(User,blank=True, null=True)

class Comment(models.Model):
    user = models.ForeignKey('user.User', blank=True, null=True, on_delete=models.CASCADE,related_name="owners")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True,related_name="comment_post")
    content = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5),MinValueValidator(1)]
        )
    