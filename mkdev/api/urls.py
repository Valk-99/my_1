from django.urls import path

from api.views import ProductsViewSet

urlpatterns = [
    path('products/', ProductsViewSet.as_view()),
]
