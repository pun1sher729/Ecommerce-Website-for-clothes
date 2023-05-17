"""
Definition of urls for Shopping_website.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
   path('', include('shop_app.urls')),
    path('admin/', admin.site.urls),
]
