from .models import *
from django import forms
# from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings



class BookForm(forms.ModelForm):

    title = forms.CharField(max_length=200, required=False, empty_value=None)
    authors__in = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        required=False,
    )

    class Meta:
        model = Book
        fields = ['title', 'pub_date', 'edition', 'volume', 'publication']


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class ProfileForm(forms.Form):
    email = forms.EmailField()
    firstname = forms.CharField(max_length=30,required=False)
    lastname = forms.CharField(max_length=150, required=False)
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,required=False)
    phone = forms.IntegerField(required=False)

