from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage

from ckeditor.widgets import CKEditorWidget

from django import forms
from .models import *


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Seller)
admin.site.register(Order)