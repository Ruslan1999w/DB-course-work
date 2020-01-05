from django import forms

from .models import Users


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('login', 'email', 'password', 'user_category')
