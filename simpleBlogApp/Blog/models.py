from django.contrib.auth.models import User
from django.db import models


class UserBlog(models.Model):
	user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_blog')
	blog_followers_ids = models.ManyToManyField(User, blank=True, null=True, related_name='followers')

	class Meta:
		db_table = 'user_blog'

	def __str__(self):
		return "{} {}'s Blog".format(self.id, self.user_id.username)


class BlogPost(models.Model):
	blog_id = models.ForeignKey(UserBlog, on_delete=models.CASCADE, related_name='posts')
	title = models.CharField(max_length=255, default=None)
	content = models.TextField(blank=True, null=True, default=None)
	date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	users_read_ids = models.ManyToManyField(User, blank=True, related_name='users_read')

	class Meta:
		db_table = 'blog_post'

	def __str__(self):
		return '{} {}'.format(self.id, self.title)

