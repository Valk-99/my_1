from django.urls import path
from django.contrib.flatpages import views as viewsf

from .views import IndexPageListView, \
    ProductByTagListView, ProfileUpdate, \
    ProductUpdate, CreateProduct, SearchResultsView, product_views, robots_txt, \
    ProductByCategoryListView, product_detail

urlpatterns = [
    path('', IndexPageListView.as_view(),
         name='index'),
    path('good/add/', CreateProduct.as_view(),
         name='product_create'),
    path('good/<int:pk>/edit/', ProductUpdate.as_view(),
         name='product_update'),
    path('good/<int:pk>/', product_detail,
         name='product_detail'),
    path('good/tag/<slug:tag_slug>/', ProductByTagListView.as_view(),
         name='tag_slug'),
    path('good/category/<slug:category_slug>/', ProductByCategoryListView.as_view(),
         name='category_slug'),


    path('accounts/profile/', ProfileUpdate.as_view(),
         name='profile'),
    # search
    path('search/', SearchResultsView.as_view(), name='search_results'),

    # Flatpages
    path('main/', viewsf.flatpage, {'url': '/main/'}, name='main'),

    path('goods/views/', product_views, name='views'),

    path("robots.txt", robots_txt),
]
