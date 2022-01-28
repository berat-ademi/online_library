from django import forms
from .models import *  #i importojm modelet



class RegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    name = forms.CharField(widget=forms.TextInput)
    address = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Customer
        fields = '__all__'


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

