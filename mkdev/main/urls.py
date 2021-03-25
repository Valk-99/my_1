from django.urls import path
from django.contrib.flatpages import views as viewsf

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('main/', viewsf.flatpage, {'url': '/main/'}, name='main'),
]