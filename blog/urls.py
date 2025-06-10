from django.urls import path
from django.contrib.auth import views as auth_views  # Этот импорт обязателен!
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('add-product/', views.add_product, name='add_product'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('blog/', views.post_list, name='post_list'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('product/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
]