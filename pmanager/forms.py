from django import forms
from .models import Sites, Credentials
from .encrypt import AESEncryption
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SitesForm(forms.ModelForm):
    class Meta:
        model = Sites
        fields = ["sitename"]


class CredentialsAddForm(forms.ModelForm):
    class Meta:
        model = Credentials
        fields = ["username", "password", "Site"]
        widgets = {"Site": forms.HiddenInput()}
    
    def clean_password(self):
        X=AESEncryption()
        password = self.cleaned_data.get('password')

        encrypted = X.encrypt_passwords("123", password)

        return encrypted

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']