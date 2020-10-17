from django.urls import re_path
from rest_framework import routers

from .views import BlogPostViewSet

router = routers.DefaultRouter()
router.register(r'post', BlogPostViewSet, 'post')

urlpatterns = router.urls
