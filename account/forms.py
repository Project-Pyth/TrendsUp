from django import forms
from django.contrib.auth.models import User
from account.models import UserProfile


# User Edit Form
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )


# UserProfile Edit Form
class PersonalEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description',
                  'city',
                  'phone',
                  'image'
                  )
