from rest_framework import generics
from rest_framework import permissions
from api.serializers import ProductsListSerializer
from main.models import Product


class ProductsViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer
    permission_classes = [permissions.IsAuthenticated]
