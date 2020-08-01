from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class registerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','password1','password2']
        # userName = forms.CharField(label='Username')
class loginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','password1']