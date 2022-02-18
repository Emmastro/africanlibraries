from django import forms
from account.models import Reader


class RegisterForm(forms.ModelForm):

	class Meta:
		model = Reader
		fields = ['username','email', 'password']
		widgets = {
		'password': forms.PasswordInput()
		}