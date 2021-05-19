from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Product, Category, Customer, \
    Seller, Order, Tag, Profile, Subscriber


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Опубликовать выбраные продукты"


def make_draft(modeladmin, request, queryset):
    queryset.update(status='d')
make_draft.short_description = "Поместить в архив выбраные продукты"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('tags', 'create_date', 'status')
    prepopulated_fields = {"slug": ("title",)}
    actions = [make_published, make_draft]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Seller)
admin.site.register(Order)
admin.site.register(Subscriber)
admin.site.register(Profile)
