from django.urls import path
from django.contrib.flatpages import views as viewsf
from django.views.decorators.cache import cache_page

from .views import IndexPageListView, ProductDetailView, ProductByTagListView, ProfileUpdate, ProfileCreate, \
    ProductUpdate, CreateProduct

urlpatterns = [
    path('', IndexPageListView.as_view(), name='index'),
    path('good/add/', CreateProduct.as_view(), name='product_create'),
    path('good/<int:pk>/edit/', ProductUpdate.as_view(), name='product_update'),
    path('good/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('good/<slug:tag_slug>/', ProductByTagListView.as_view(), name='tag_slug'),

    path('accounts/profile/create/', ProfileCreate.as_view(), name='profile_form'),
    path('accounts/profile/<int:pk>/', ProfileUpdate.as_view(), name='profile'),

    # Flatpages
    path('main/', viewsf.flatpage, {'url': '/main/'}, name='main'),
]
