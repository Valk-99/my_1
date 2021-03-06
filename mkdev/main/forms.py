from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from main.models import Profile, Product, Comment


def validate_age(age):
    if age < 18:
        raise ValidationError(_(
            '%(age) s должно быть больше чем 18'),
                              params={'age': age},)


class ProfileForm(forms.ModelForm):
    how_old = forms.IntegerField(validators=[validate_age],
                                 widget=forms.NumberInput(
                                     attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=160, widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=160, widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
                                     attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'how_old']


class ProductCreateUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=30,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control'}))
    slug = forms.SlugField(max_length=30,
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'}))
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = '__all__'


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ['body']

