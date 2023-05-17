from django.urls import path
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        path('', views.index, name='index'),
        path('user_signup', views.user_signup_view, name='user_signup_view'),
        path('user_login', views.user_login_view, name='user_login_view'),
        path('logout', views.logout, name='logout'),
        path('seller_signup', views.seller_signup_view, name='seller_signup_view'),
        path('seller_login', views.seller_login_view, name='seller_login_view'),
        path('add_product', views.add_product_view, name='add_product_view'),
        path('male_category', views.male_category_view, name='male_category_view'),
        path('female_category', views.female_category_view, name='female_category_view'),
        path('add_to_cart', views.add_to_cart_view, name='add_to_cart_view'),
        path('view_cart', views.view_cart, name='view_cart'),
        path('search', views.search, name='search'),
        path('seller_logout', views.seller_logout, name='seller_logout'),
        path('seller_home', views.seller_home, name='seller_home'),
        path('list_seller_products', views.list_seller_products, name='list_seller_products'),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)