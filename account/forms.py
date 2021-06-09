from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    # For profile
    bio = forms.CharField(max_length=254, required=False, help_text='Optional. Max Lengh: 254.')
    location = forms.CharField(max_length=254, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'bio',
            'location',
            'password1',
            'password2',
        )


class UpdateForm(UserChangeForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    # For profile
    bio = forms.CharField(max_length=254, required=False, help_text='Optional. Max Lengh: 254.')
    location = forms.CharField(max_length=254, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = (
            'email',
            'bio',
            'location',
        )
