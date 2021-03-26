from django.urls import path
from django.contrib.flatpages import views as viewsf

from .views import IndexPageListView, ProductDetailView

urlpatterns = [
    path('', IndexPageListView.as_view(), name='index'),
    path('good/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    # Flatpages
    path('main/', viewsf.flatpage, {'url': '/main/'}, name='main'),
]