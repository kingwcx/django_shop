from django import forms

from .models import User
from django.contrib.auth import get_user_model

class LoginForm(forms.ModelForm):
	username = forms.CharField(max_length=150)
	class Meta:
		model = get_user_model()
		fields = ['password']

class RegisterForm(forms.ModelForm):
	username = forms.CharField(max_length=150)
	re_password = forms.CharField(max_length=12)
	class Meta:
		model = get_user_model()
		fields = ['password']

	def clean_useranme(self):
		username = self.cleaned_data.get('username')
		exists = User.objects.filter(username=username).exists()
		if exists:
			raise forms.ValidationError("用户名已经存在！")
		return username

	def clean(self):
		cleaned_data = super().clean()
		pwd1 = cleaned_data.get('password')
		pwd2 = cleaned_data.get('re_password')
		if pwd1 != pwd2:
			raise forms.ValidationError('两个密码不一致！')
		return cleaned_data