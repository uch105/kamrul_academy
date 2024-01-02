from django import forms
from .models import Signed_user

class UserPictureForm(forms.ModelForm):
    class Meta:
        model = Signed_user
        fields = ['pp']