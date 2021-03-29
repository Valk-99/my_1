from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from main.forms import ProfileForm
from main.models import Product, Tag, Profile


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


class ProfileCreate(CreateView):
    """Создание профиля пользователя"""
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'

    def get_initial(self):
        # этод метод я оставил только при создании так как связку User-Profile надо устанавливать
        # только при создании профиля, при редактировании профиля она уже будет и заново устанавливать не надо
        initial = super(ProfileCreate, self).get_initial()
        initial['user'] = self.request.user.id
        return initial


class ProfileUpdate(LoginRequiredMixin,UpdateView):
    model = Profile
    login_url = 'index'
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('index')



