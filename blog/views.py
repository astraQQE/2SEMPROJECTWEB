from django.shortcuts import render
from .models import Product, Review, Advertisement


def home(request):
    # Популярные товары (фильтрация)
    popular_products = Product.objects.filter(stock__gt=0).order_by('-created')[:6]
    # Последние обзоры (сортировка)
    latest_reviews = Review.objects.all().order_by('-created_at')[:3]
    # Активные акции (агрегация)
    active_ads = Advertisement.objects.filter(status='active')

    return render(request, 'blog/index.html', {
        'popular_products': popular_products,
        'latest_reviews': latest_reviews,
        'active_ads': active_ads
    })

def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = []
    return render(request, 'blog/search.html', {'results': results})