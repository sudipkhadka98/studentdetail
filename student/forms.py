from django import forms
from .models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Studentform(forms.ModelForm):
    class Meta:
        model=Student
        fields=["rollno","firstname","lastname","address","phone","gender"]

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]