from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from .models import BlogPost


@receiver(post_save, sender=BlogPost)
def send_mail_message(sender, **kwargs):
	"""
		method for sending email for followers
		after user create new post
	"""

	if kwargs.get('created'):

		followers_emails = kwargs.get('instance').blog_id.blog_followers_ids.all().values('email')

		recipients_email_list = []

		for item in followers_emails:
			if item.get('email'):
				recipients_email_list.append(item.get('email'))

		if recipients_email_list:
			user = kwargs.get('instance').blog_id.user_id.username
			post_id = kwargs.get('instance').id

			subject = f'{user} create new post'
			message = f'You can see new post here: \n http://localhost:8080/#/post/{post_id}/'
			sender_email = 'Kostenko.rob@gmail.com'

			send_mail(subject, message, sender_email, recipients_email_list, fail_silently=False)

