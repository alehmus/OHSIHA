from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# luokka rekisteröitymislomakkeelle
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# luokka käyttäjän tietojen päivittämiseksi
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# luokka Profiilin päivittämiseen
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # uuset luotavat parametrit
        fields = ['linja', 'pysakki']
