from django.urls import path
from django.contrib.flatpages import views as viewsf

from .views import IndexPageListView, ProductDetailView, ProductByTagListView, ProfileUpdate

urlpatterns = [
    path('', IndexPageListView.as_view(), name='index'),
    path('good/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('good/<slug:tag_slug>/', ProductByTagListView.as_view(), name='tag_slug'),
    # accounts
    path('accounts/profile/<int:pk>/', ProfileUpdate.as_view(), name='profile'),

    # Flatpages
    path('main/', viewsf.flatpage, {'url': '/main/'}, name='main'),
]