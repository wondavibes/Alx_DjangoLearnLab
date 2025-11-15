from .models import Book
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "date_of_birth",
            "profile_photo",
            "password1",
            "password2",
        )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]
