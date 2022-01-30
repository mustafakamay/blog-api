from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('post', PostViewSet)
router.register('comment',CommentViewSet)
router.register('favorite',FavoritePostViewSet)
app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
