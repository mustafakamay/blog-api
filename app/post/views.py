from email import header
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY,HTTP_204_NO_CONTENT
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, viewsets, generics
from rest_framework.response import Response

from app.settings import SECRET_KEY
from .models import *
from .serializers import *
import sys
import jwt

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        print(user)
        data["user"]=user.id
        
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if instance.user != user:
            return Response("You are not authorized to perform this action",status=400)
        serializer = self.get_serializer(instance,data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response("Deleted successfully",status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve' or self.action == 'list':
            return PostListSerializer
        else:
            return PostSerializer


class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):

        access_token =request.headers['Authorization'].split(" ")[1]
        header_data = jwt.get_unverified_header(access_token)
        payload = jwt.decode(access_token,SECRET_KEY, algorithms=[header_data['alg']])
        data = request.data
        data["user"] = payload["user_id"]
        user = request.user
        
        if data["user"] != payload["user_id"]:
            return Response("You cannot comment on behalf of someone else.",status=403)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Deleted successfully",status=204)


    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve' or self.action == 'list':
            return CommentListSerializer
        else:
            return CommentSerializer
    def list(self,request,*args,**kwargs):
        comment_list = Comment.objects.filter(user__id=request.user.id)

        return Response(CommentListSerializer(comment_list,many=True).data,status=status.HTTP_200_OK)


class FavoritePostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

    def update(self,request,*args,**kwargs):
        instance = self.get_object()
        instance.favorited_by.add(request.user)
        if instance.user == request.user:
            return Response("You can not add favorite your post",status=status.HTTP_400_BAD_REQUEST)

        return Response("Succesfully added favorite",status=200)

    def destroy(self,request,*args,**kwargs):
        instance = self.get_object()
        instance.favorited_by.remove(request.user)

        return Response("Succesfully removed favorite",status=status.HTTP_204_NO_CONTENT)

    def list(self,request,*args,**kwargs):
        favorited_post = Post.objects.filter(favorited_by__id__exact=request.user.id)

        return Response(PostSerializer(favorited_post,many=True).data,status=200)
