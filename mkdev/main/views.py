from datetime import datetime

from allauth.account.views import SignupView
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView,\
    UpdateView, CreateView
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector

from main.forms import ProfileForm, ProductCreateUpdateForm
from main.models import Product, Tag, Profile, ProductViews


class IndexPageListView(ListView):
    model = Product
    paginate_by = 6
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
        context['views'] = cache.get_or_set('views', self.object.views, 60)
        return context

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        object.views = int(object.views) + 1
        object.save()
        return super(ProductDetailView, self).get(self,
                                                  request, *args, **kwargs)


class ProductByTagListView(ListView):
    model = Product
    template_name = 'main/tag_product.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        context['Tag'] = Tag.objects.all()
        context['tag_title'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return context

    def get_queryset(self):
        return Product.objects.filter(tags__slug=self.kwargs['tag_slug'])


class ProfileCreate(LoginRequiredMixin, CreateView):
    """Создание профиля пользователя"""
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'

    def get_initial(self):
        # этод метод я оставил только при
        # создании так как связку User-Profile надо устанавливать
        # только при создании профиля, при редактировании
        # профиля она уже будет и заново устанавливать не надо
        initial = super(ProfileCreate, self).get_initial()
        initial['user'] = self.request.user.id
        return initial


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    login_url = 'index'
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('index')


class CreateProduct(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'main.add_product'
    login_url = 'index'
    model = Product
    form_class = ProductCreateUpdateForm
    template_name = 'main/product_form.html'

    def form_valid(self, form):
        form.instance.send_email()
        form.instance.save()
        return super().form_valid(form)


class ProductUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'main.change_product'
    login_url = 'index'
    model = Product
    form_class = ProductCreateUpdateForm
    template_name = 'main/product_update_form.html'


class MySignupView(SignupView):
    pass

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            instance.groups.add(Group.objects.get_or_create(
                name='common users')[0]
                                )


class SearchResultsView(ListView):
    model = Product
    template_name = 'main/search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        vector = SearchVector('title', 'description')
        object_list = Product.objects.annotate(search=vector).filter(search=query)
        return object_list

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        context['Tag'] = Tag.objects.all()
        return context


def product_views(request):
    views_of_product = ProductViews.objects.order_by('-views')
    return render(request, 'main/views.html', {'views_of_product': views_of_product})
