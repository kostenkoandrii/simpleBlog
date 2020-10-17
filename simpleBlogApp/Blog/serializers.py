from rest_framework import serializers

from .models import BlogPost


class BlogPostModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogPost
		fields = ['id', 'blog_id', 'users_read_ids', 'tittle', 'content', 'date_created']
