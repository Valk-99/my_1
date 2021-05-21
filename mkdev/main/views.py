from datetime import datetime

from allauth.account.views import SignupView
from django.contrib.auth.mixins import LoginRequiredMixin,\
    PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView,\
    UpdateView, CreateView
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector
from django.views.generic.edit import FormMixin

from main.forms import ProfileForm, ProductCreateUpdateForm, CommentForm
from main.models import Product, Tag, Profile, ProductViews, Category, Comment


class IndexPageListView(ListView):
    model = Product
    paginate_by = 6
    template_name = 'main/index.html'
    context_object_name = 'products'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turn_on_block'] = True
        context['now'] = datetime.now()
        context['tag'] = Tag.objects.all()
        context['cat'] = Category.objects.all()
        return context


def product_detail(request, pk):
    template_name = 'main/product_detail.html'
    now = datetime.now()
    tag = Tag.objects.all()
    cat = Category.objects.all()
    product = get_object_or_404(Product, pk=pk)
    views_cache = cache.get_or_set('views', product.views, 60)
    product.views = views_cache + 1
    product.save()
    comments = product.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = form.save(commit=False)
            # Assign the current post to the comment
            new_comment.product = product
            new_comment.username = request.user.username
            # Save the comment to the database
            new_comment.save()
    else:
        form = CommentForm()

    return render(request, template_name, {'product': product,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'form': form, 'now': now,
                                           'cat': cat, 'tag': tag})

# class ProductDetailView(FormMixin, DetailView):
#     model = Product
#     template_name = 'main/product_detail.html'
#     form_class = CommentForm
#     success_url = 'product_detail'
#
#     def form_valid(self, form):
#         product = get_object_or_404(Product, id=self.kwargs['id'])
#         form.instance.post = product
#         return super().form_valid(form)
#
#     def get_context_data(self, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['turn_on_block'] = True
#         context['now'] = datetime.now()
#         context['Tag'] = Tag.objects.all()
#         context['Cat'] = Category.objects.all()
#         context['new_comment '] = None
#         context['views'] = cache.get_or_set('views', self.object.views, 60)
#         return context
#
#     def get(self, request, *args, **kwargs):
#         object = self.get_object()
#         object.views = int(object.views) + 1
#         object.save()
#         return super(ProductDetailView, self).get(self,
#                                                   request, *args, **kwargs)


class ProductByTagListView(ListView):
    model = Product
    template_name = 'main/tag_product.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        context['tag'] = Tag.objects.all()
        context['cat'] = Category.objects.all()
        context['tag_title'] = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return context

    def get_queryset(self):
        return Product.objects.filter(tags__slug=self.kwargs['tag_slug'])


class ProductByCategoryListView(ListView):
    model = Product
    template_name = 'main/cat_product.html'
    paginate_by = 10
    context_object_name = 'products'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        context['tag'] = Tag.objects.all()
        context['cat'] = Category.objects.all()
        context['category_title'] = Category.objects.get(slug=self.kwargs['category_slug'])
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    login_url = 'index'
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.request.user.id)


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
        context['tag'] = Tag.objects.all()
        context['cat'] = Category.objects.all()
        return context


def product_views(request):
    views_of_product = ProductViews.objects.order_by('-views')
    return render(request, 'main/views.html', {'views_of_product': views_of_product})


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /private/",
        "Disallow: /junk/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
