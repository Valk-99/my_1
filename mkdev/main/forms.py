from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from main.models import Profile, Product
from main.tasks import send_email_task_product


def validate_age(age):
    if age < 18:
        raise ValidationError(_('%(age) s должно быть больше чем 18'),
                              params={'age': age}, )


class ProfileForm(forms.ModelForm):
    how_old = forms.IntegerField(validators=[validate_age],widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['user_profile','how_old']


class ProductCreateUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.SlugField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def send_email(self):
        send_email_task_product.delay(
            self.cleaned_data['title'], self.cleaned_data['slug'],
            self.cleaned_data['description'], self.cleaned_data['price']
        )

    class Meta:
        model = Product
        fields = '__all__'