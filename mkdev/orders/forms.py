from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=160, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=160, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=160, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=160, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    address_of_postal = forms.CharField(max_length=160, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=160, widget=forms.TextInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address_of_postal', 'city']
