from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList

from posts.models import profile_c

class sign_up_form_c(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields=('username', 'email',  'password1', 'password2')

class profile_edit_form_c(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = profile_c
        fields=('date_of_birth', 'location', 'gender', 'profession', 'profile_image')
        # widgets = {'profile_image': forms.ClearableFileInput }

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        ff = getattr(self.instance, 'profile_image')
        result = ff.__class__(self.instance, ff.field, ff.name)
        self.fields['profile_image'].render_image = 1
        self.fields['profile_image'].render_image_url=self.instance.thumb_url




