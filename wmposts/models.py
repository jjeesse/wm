from django.db import models
from wmuser.models import BaseUser
from datetime import datetime
#from django.contrib.auth.models import User

class BasePost(models.Model):
	# Link to a user. Field references at https://docs.djangoproject.com/en/1.8/ref/models/fields/
	uploader = models.ForeignKey('wmuser.BaseUser')
	
	# Additional Fields
	title = models.CharField(max_length=256, default="This is a title")
	post_content = models.ImageField(upload_to="static/posts_main", default="posts_main/placeholder.jpg")
	date_added = models.DateTimeField(default=datetime.now, blank=True)
	upvotes = models.PositiveIntegerField(default=0)
	noc = models.PositiveIntegerField(default=0)

	# Admin Return
	def __str__(self):
		return self.title


