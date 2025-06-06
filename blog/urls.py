from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),  # Для поиска
]