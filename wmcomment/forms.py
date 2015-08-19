from django import forms
from django.forms import ModelForm, Textarea
from wmcomment.models import BaseComment, NestedComment

class CommentForm(ModelForm):
	class Meta: 
		model = BaseComment
		fields = ['comment_content']

class NestedCommentForm(ModelForm):
	class Meta:
		model = NestedComment
		fields = ['nested_content']