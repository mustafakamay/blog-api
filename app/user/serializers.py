
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from user.models import User


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserRegisterSerializer(ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {"password": {"write_only": True},
                        "email": {"required": True}}

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do no match!")
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name', "")
        last_name = validated_data.get('last_name', "")
        password = validated_data.get('password')
        user_obj = User(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.save()

        data = user_obj
        return data

    def get_groups(self, obj):
        groups = obj.groups.all()
        g = [group.name for group in groups]
        return g



class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]
        read_only_fields = ('id',)

class UserListLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]
        read_only_fields = ('id',)


class UserLoginReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]
        read_only_fields = ('id','password')


class UserListDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password',)
        read_only_fields = ('id',)


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = CharField(write_only=True, required=True)
    user = UserLoginReturnSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'token',
            'user',

        ]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def validate(self, data):
        password = data.get("password")
        email = data.get("email")
        user = User.objects.filter(email=email).distinct()
        if user.exists():
            user_obj = user.first()
        else:
            raise ValidationError("Incorrect credential")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError({"detail": "Incorrect credential"})
        payload = JWT_PAYLOAD_HANDLER(user_obj)
        token = JWT_ENCODE_HANDLER(payload)
        data["token"] = token
        data["user"] = UserLoginReturnSerializer(user_obj).data
        return data

