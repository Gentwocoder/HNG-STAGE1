from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('strings', include('strings.urls')),
    # re_path(r'^strings/?$', include('strings.urls')),
]
