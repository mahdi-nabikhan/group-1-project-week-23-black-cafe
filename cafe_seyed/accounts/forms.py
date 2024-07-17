from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth import authenticate

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=20)
    password2 = forms.CharField(label='Password_confirm', widget=forms.PasswordInput, max_length=20)

    class Meta:
        model = CustomUser

        fields = ['first_name', 'last_name', 'email', 'age', 'city']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords must match')
        return cd['password2']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'age', 'city']
