from django.db import models
from wmposts.models import BasePost
from wmuser.models import BaseUser
from datetime import datetime

class BaseComment(models.Model):
	# Link to a post and a user. Field references at https://docs.djangoproject.com/en/1.8/ref/models/fields/
	linked_post = models.ForeignKey('wmposts.BasePost')
	linked_user = models.ForeignKey('wmuser.BaseUser')

	# Additional Fields
	comment_content = models.TextField()
	posted_on = models.DateTimeField(default=datetime.now, blank=True)
	comment_upvotes = models.IntegerField(default=0)

	def __str__(self):
		return str(self.comment_content)

class NestedComment(models.Model):
	# Link to a comment and a user. Field references at https://docs.djangoproject.com/en/1.8/ref/models/fields/
	nested_linked_user = models.ForeignKey('wmuser.BaseUser')
	nested_linked_comment = models.ForeignKey('BaseComment', related_name="nested_under")

	# Additional Fields
	nested_content = models.TextField()
	nested_posted_on = models.DateTimeField(default=datetime.now, blank=True)
	nested_comment_upvotes = models.IntegerField(default=0)

	def __str__(self):
		return str(self.nested_linked_comment)






