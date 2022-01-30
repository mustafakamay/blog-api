from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.utils import json
from rest_framework.decorators import action

from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        email = serializer.data.get("email")
        user = User.objects.filter(email=email).first()

        headers = self.get_success_headers(serializer.data)
        serializer2 = UserListSerializer(user)
        return Response(serializer2.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["POST"])
    def login(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):

            res = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
            }
            new_data = serializer.data
            res.update(new_data)
            return Response(res, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Deleted successfully",status=200)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'retrieve':
            return UserListDetailSerializer
        else:
            return UserListSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'login':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
