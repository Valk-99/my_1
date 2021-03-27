
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from main.models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField()

    def validate_age(self, age):
        if age <= 18:
            raise ValidationError(_('%(age) should be more than 18'),
                                  params={'age': age}, )

    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'age']