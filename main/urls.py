from django.contrib.flatpages import views
from django.urls import path


urlpatterns = [
    path('main/', views.flatpage, {'url': '/main/'}, name='main'),
]