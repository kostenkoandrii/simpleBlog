from django.contrib.auth.models import User
from rest_framework import serializers

from .models import BlogPost, UserBlog


class BlogPostModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogPost
		fields = ['id', 'blog_id', 'users_read_ids', 'title', 'content', 'date_created']


class UserModelSerializer(serializers.ModelSerializer):
	blog_id = serializers.SerializerMethodField()
	followed_blogs = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ['id', 'username', 'blog_id', 'followed_blogs']

	def get_followed_blogs(self, obj):
		return ','.join([str(item.get('id')) for item in obj.followers.all().values('id')])

	def get_blog_id(self, obj):
		return obj.user_blog.id


class UserBlogModelSerializer(serializers.ModelSerializer):
	username = serializers.SerializerMethodField()

	class Meta:
		model = UserBlog
		fields = ['id', 'user_id', 'username', 'blog_followers_ids']

	def get_username(self, obj):
		return obj.user_id.username
