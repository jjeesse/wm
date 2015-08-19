from django import forms
from django.forms import ModelForm
from wmposts.models import BasePost

class UploadFileForm(ModelForm):
	class Meta:
		model = BasePost
		fields = ['title', 'post_content']#, 'uploader' 
		
	
 	