from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    User, Category, Brand, Product, Order, OrderProduct,
    Review
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_registered', 'role')
    list_filter = ('role', 'date_registered')
    search_fields = ('username', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'image_preview')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'description')
    raw_id_fields = ('category','brand')

    @admin.display(description=_('Изображение'))
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" />', obj.image.url)
        return _("Нет изображения")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username')