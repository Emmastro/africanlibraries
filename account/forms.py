from django.contrib.auth.forms import  AuthenticationForm
from django import forms
from account.models import Reader, Administrator

from django import forms


class LoginForm(AuthenticationForm):
	
	
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Username ...'

		self.fields['password'].widget.attrs['class'] = 'form-control'
		self.fields['password'].widget.attrs['placeholder'] = 'Password ...'

class RegistrationForm(forms.ModelForm):

    class Meta:

        model = Administrator
        fields = ('username', 'first_name', 'last_name', 'school')
    

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ('first_name', 'last_name', 'username', 'email', )
    