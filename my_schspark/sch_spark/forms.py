from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput, TextInput



#create a user (model)

class CreateUserForm(UserCreationForm):

     class Meta:

          model = User
          fields = ['username', 'email', 'password1', 'password2']
         
#Authenticate a user 9(Model form)        

class LoginForm(AuthenticationForm):
    username = forms.CharField (widget=TextInput())
    password = forms.CharField(widget=PasswordInput())