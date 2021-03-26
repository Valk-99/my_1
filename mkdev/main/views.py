from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from main.models import Product, Tag


class IndexPageListView(ListView):
    model = Product
    template_name = 'main/index.html'
    context_object_name = 'products'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turn_on_block'] = True
        context['now'] = datetime.now()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product_detail.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turn_on_block'] = True
        context['now'] = datetime.now()
        return context