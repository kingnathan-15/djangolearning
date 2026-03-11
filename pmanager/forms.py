from django import forms
from .models import Sites, Credentials
from .encrypt import AESEncryption
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SitesForm(forms.ModelForm):
    class Meta:
        model = Sites
        fields = ["sitename", "user"]
        widgets = {"user": forms.HiddenInput()}


class CredentialsAddForm(forms.ModelForm):
    class Meta:
        model = Credentials
        fields = ["username", "password", "Site"]
        widgets = {"Site": forms.HiddenInput()}
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        X = AESEncryption()
        password = self.cleaned_data.get('password')

        if not self.request:
            raise forms.ValidationError("Request is required to encrypt password")

        authstring = self.request.user.username + self.request.user.password
        encrypted = X.encrypt_passwords(str(authstring), password)

        return encrypted

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-input'
        })
    )