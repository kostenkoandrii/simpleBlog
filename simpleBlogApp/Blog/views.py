from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from .api_filters import PostsFilter
from .models import BlogPost, UserBlog
from .serializers import BlogPostModelSerializer, UserModelSerializer, UserBlogModelSerializer


class BlogPostViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin,
					  mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):

	permission_classes = [AllowAny]
	filterset_class = PostsFilter
	serializer_class = BlogPostModelSerializer
	queryset = BlogPost.objects.all().order_by('-date_created')

	def update(self, request, *args, **kwargs):
		"""
			method for update read-status to current post by user,
		"""
		user_id = request.data.get('user_id')

		try:
			user = User.objects.get(id=user_id)
		except ObjectDoesNotExist:
			return Response({"message": ["error"]}, status=status.HTTP_400_BAD_REQUEST)

		instance = self.get_object()
		read_users = instance.users_read_ids

		if user in read_users.all():
			read_users.remove(user)
			instance.save()
		else:
			read_users.add(user)
			instance.save()

		return Response({"message": "OK"}, status=status.HTTP_200_OK)


class CheckUserExistsViewSet(mixins.RetrieveModelMixin, GenericViewSet):

	permission_classes = [AllowAny]
	serializer_class = UserModelSerializer
	queryset = User.objects.all()
	lookup_field = 'username'


class UserBlogViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, GenericViewSet):

	permission_classes = [AllowAny]
	serializer_class = UserBlogModelSerializer

	def get_queryset(self):
		"""
			:return: UsersBlogs objects without self UserBlog
			because user doesn't need to follow himself
		"""
		blog_id = self.request.query_params.get('blog_id')
		return UserBlog.objects.exclude(id=blog_id)

	def update(self, request, *args, **kwargs):
		"""
			method for update follow-status to current blog by user,
			also  it deleting read-status of post, when user make unfollow
			from blog
		"""
		user_id = request.data.get('user_id')

		try:
			user = User.objects.get(id=user_id)
		except ObjectDoesNotExist:
			return Response({"message": ["error"]}, status=status.HTTP_400_BAD_REQUEST)

		instance = self.get_object()
		followed_users = instance.blog_followers_ids

		for post in instance.posts.all():
			if user in post.users_read_ids.all():
				post.users_read_ids.remove(user)

		if user in followed_users.all():
			# unfollow from blog by user
			followed_users.remove(user)
			instance.save()

			# deleting read-status from post by user
			for post in instance.posts.all():
				if user in post.users_read_ids.all():
					post.users_read_ids.remove(user)
					post.save()
		else:
			# follow blog by user
			followed_users.add(user)
			instance.save()

		return Response({"message": "OK"}, status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin, GenericViewSet):

	permission_classes = [AllowAny]
	serializer_class = UserModelSerializer
	queryset = User.objects.all()
	lookup_field = 'user_blog'
