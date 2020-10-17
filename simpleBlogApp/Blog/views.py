from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import BlogPost
from .serializers import BlogPostModelSerializer


class BlogPostViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = BlogPostModelSerializer
    queryset = BlogPost.objects.all()
