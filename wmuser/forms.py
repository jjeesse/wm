from django.contrib.auth.models import User
from django.forms import ModelForm
from wmuser.models import BaseUser
from django import forms

class SignupForm(ModelForm):
	class Meta:
		model = BaseUser
		fields = ['username', 'email', 'password']

class ProfileForm(ModelForm):
	class Meta: 
		model = BaseUser
		fields = []


class UploadProfilePicForm(ModelForm):
	class Meta:
		model = BaseUser
		fields = ['profile_pic']
		
		
class ForgotPasswordForm(ModelForm):	
	class Meta:
		model = BaseUser
		fields = ['username', 'email']