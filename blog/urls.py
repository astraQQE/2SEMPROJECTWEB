from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('add-product/', views.add_product, name='add_product'),
]