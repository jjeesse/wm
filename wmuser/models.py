from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class BaseUser(AbstractUser):
	
	# Additional fields
	profile_pic = models.ImageField(upload_to='static/profile_pics', default="static/profile_pics/user-placeholder.png")
	balance = models.IntegerField(default=10)
	custom_like_value = models.IntegerField(default=1)
	
	# Return for AdminSite 
	def __str__ (self):
		return self.username

