from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    # For profile
    birth_day = forms.DateField(required=False, help_text='Optional. Format: YYYY-MM-DD')
    bio = forms.CharField(max_length=254, required=False, help_text='Optional. Max Lengh: 254.')
    location = forms.CharField(max_length=254, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'birth_day',
            'email',
            'bio',
            'location',
            'password1',
            'password2',
        )
