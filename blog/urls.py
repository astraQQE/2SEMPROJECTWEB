from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('add-product/', views.add_product, name='add_product'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:product_id>/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('blog/', views.post_list, name='post_list'),
]