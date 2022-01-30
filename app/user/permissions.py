from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

class IsAdminPermission(BasePermission):


    def has_permission(self, request, view):

        if request.method == 'get' or request.method == 'GET':
            return True
        else:
            if request.user.groups.filter(name="admin").exists():
                return True
        return False