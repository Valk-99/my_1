from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('main.urls')),
    path('accounts/', include('allauth.urls')),
]