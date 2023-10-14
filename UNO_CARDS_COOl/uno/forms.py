from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class NameForm(forms.Form):
    name = forms.CharField(label = '', max_length = 1000, widget=forms.TextInput(attrs={'class': 'text', 'id' : 'name', 'placeholder' : 'иван228777'}))