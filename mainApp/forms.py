from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from mainApp.models import Films, Categories


class RegistrationForm(UserCreationForm):
    error_css_class = 'has-error'
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'is_superuser']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Films
        fields = ['category', 'name', 'image', 'preview', 'desc']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'desc']