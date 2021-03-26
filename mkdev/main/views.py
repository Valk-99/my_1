from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from main.models import Product, Tag


class IndexPageListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'main/index.html'
    context_object_name = 'products'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turn_on_block'] = True
        context['now'] = datetime.now()
        context['Tag'] = Tag.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turn_on_block'] = True
        context['now'] = datetime.now()
        context['Tag'] = Tag.objects.all()
        return context


class ProductByTagListView(ListView):
    model = Product
    template_name = 'main/tag_product.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Tag'] = Tag.objects.all()
        context['tag_title'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return context

    def get_queryset(self):
        return Product.objects.filter(tags__slug=self.kwargs['tag_slug'])
