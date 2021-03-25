from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage

from ckeditor.widgets import CKEditorWidget

from django import forms


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
