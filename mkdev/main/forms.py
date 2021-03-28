from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from main.models import Profile


def validate_age(age):
    if age < 18:
        raise ValidationError(_('%(age) s должно быть больше чем 18'),
                              params={'age': age}, )


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    how_old = forms.IntegerField(validators=[validate_age],widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'how_old']