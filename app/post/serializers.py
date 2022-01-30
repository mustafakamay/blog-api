from rest_framework import serializers

from user.serializers import UserListSerializer
from .models import Post,Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('id',)
        depth=0


class PostListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('id',)
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('id',)
        depth=0

class CommentListSerializer(serializers.ModelSerializer):
    user =UserListSerializer()

    class Meta:
        model = Comment
        fields = "__all__"