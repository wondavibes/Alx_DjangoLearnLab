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


class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100)
    another_field = forms.IntegerField()
    optional_field = forms.EmailField(required=False)
    choice_field = forms.ChoiceField(
        choices=[("option1", "Option 1"), ("option2", "Option 2")]
    )
    date_field = forms.DateField(widget=forms.SelectDateWidget)
