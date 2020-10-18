from django.urls import re_path
from rest_framework import routers

from .views import BlogPostViewSet, CheckUserExistsViewSet, UserBlogViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'post', BlogPostViewSet, 'post')
router.register(r'login', CheckUserExistsViewSet, 'post')
router.register(r'user_blog', UserBlogViewSet, 'user_blog')
router.register(r'user', UserViewSet, 'user')

urlpatterns = router.urls
