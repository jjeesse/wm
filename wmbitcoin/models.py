from django.db import models
from wmuser.models import BaseUser
from wmposts.models import BasePost
from wmcomment.models import BaseComment, NestedComment
#from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User


'''
class Account(models.Model):
	# Link to a user. Field references at https://docs.djangoproject.com/en/1.8/ref/models/fields/
	account_holder = models.OneToOneField('wmuser.BaseUser', related_name="holders")

	# Additional Fields
	balance = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.account_holder + ", " + self.balance'
		'''
class NestedCommentTransaction(models.Model):
	# Link to users(2) + relatedpost. Field references at https://docs.djangoproject.com/en/1.8/ref/models/fields/
	sender = models.ForeignKey('wmuser.BaseUser', related_name="nested_comment_sent_by")
	recipient = models.ForeignKey('wmuser.BaseUser', related_name="nested_comment_received_by")
	related_nested_comment = models.ForeignKey('wmcomment.NestedComment', related_name="nested_comment")

	# Additional Fields
	date_sent = models.DateTimeField(default=timezone.now, blank=True)

	def __str__(self):
		return self.sender.username + ", " + self.recipient.username

class CommentTransaction(models.Model):
	# Link to users(2) + relatedpost. Field references at https://docs.djangoproject.com/en/1.8/ref/models/fields/
	sender = models.ForeignKey('wmuser.BaseUser', related_name="comment_sent_by")
	recipient = models.ForeignKey('wmuser.BaseUser', related_name="comment_received_by")
	related_comment = models.ForeignKey('wmcomment.BaseComment', related_name="linked_comment")

	# Additional Fields
	date_sent = models.DateTimeField(default=timezone.now, blank=True)

	def __str__(self):
		return self.sender.username + ", " + self.recipient.username

class Transaction(models.Model):
	# Link to users(2) + relatedpost. Field references at https://docs.djangoproject.com/en/1.8/ref/models/fields/
	sender = models.ForeignKey('wmuser.BaseUser', related_name="sent_by")
	recipient = models.ForeignKey('wmuser.BaseUser', related_name="received_by")
	related_post = models.ForeignKey('wmposts.BasePost', related_name="linked_post")

	# Additional Fields
	date_sent = models.DateTimeField(default=timezone.now, blank=True)

	def __str__(self):
		return self.sender.username + ", " + self.recipient.username

class Withdrawal(models.Model):
	# Regular Fields
	address = models.CharField(max_length=64)
	date_withdrawn = models.DateTimeField(default=timezone.now, blank=True)

	def __str__(self):
		return self.address + ", " + self.date_withdrawn

#Deposittia varten luotava id, poistetaan kannasta kun tilaus on maksettu
class TransactionID(models.Model):
	tid = models.CharField(default="",max_length=36,unique = True) 
	user = models.ForeignKey('wmuser.BaseUser') ## one to one jos haluaa etta on vain yksi maksu kerrallaan voimassa. Kokeilun ajaksi ainakin foreign	
	amount = models.FloatField()
	status = models.IntegerField(default=0)
#	created_at = models.DateTimeField(default=timezone.now, blank=True) 
#	expires_at = models.DateTimeField(default=timezone.now, blank=True) 
	
	def __str__(self):
		return self.tid
