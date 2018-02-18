from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from posts.models import profile_c


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields=('username', 'email',  'password1', 'password2')

class profile_edit_form_c(forms.ModelForm):
    class Meta:
        model = profile_c
        fields=('date_of_birth', 'location', 'gender', 'profession')

