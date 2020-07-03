from django import forms
from django.contrib.auth.models import User
from .models import Customer

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')

class CustomerForm(forms.ModelForm):
    class Meta():
        model = Customer
        fields = ('email',)