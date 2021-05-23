from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage
from django import forms

from ckeditor.widgets import CKEditorWidget

from orders.models import Order, OrderItem
from .models import Product, Category, \
    Seller, Tag, Profile, Subscriber, Comment


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'body', 'product', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Seller)
admin.site.register(Subscriber)
admin.site.register(Profile)
