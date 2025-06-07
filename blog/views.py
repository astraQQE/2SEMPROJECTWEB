from django.shortcuts import render
from .models import Product, Review, Advertisement,Category
from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product
from django.contrib.postgres.search import TrigramSimilarity

def home(request):
    # 1. Популярные товары (используется filter() и order_by())
    popular_products = Product.objects.filter(stock__gt=0).order_by('-created')[:6]

    # 2. Последние обзоры (используется order_by())
    latest_reviews = Review.objects.all().order_by('-created_at')[:3]

    # 3. Активные акции (используется filter())
    active_ads = Advertisement.objects.filter(status='active')

    # 4. Товары с максимальным рейтингом (агрегатная функция Avg)
    top_rated_products = Product.objects.annotate(
        avg_rating=Avg('review__rating')
    ).filter(avg_rating__gte=4.5).order_by('-avg_rating')[:3]

    return render(request, 'blog/index.html', {
        'popular_products': popular_products,
        'latest_reviews': latest_reviews,
        'active_ads': active_ads,
        'top_rated_products': top_rated_products,
    })



# blog/views.py


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Точное совпадение (регистронезависимое)
        results = Product.objects.filter(name__iexact=query)

    return render(request, 'blog/search_results.html', {
        'query': query,
        'results': results,
    })
def category_detail(request, category_id):
    # Логика для отображения товаров категории
    pass

def favorites(request):
    # Логика для отображения избранных товаров
    pass

def add_product(request):
    # Логика для добавления товара (только для админов)
    pass

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему.')
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Отзывы для данного товара
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    # Похожие товары (например, из той же категории)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    return render(request, 'blog/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'similar_products': similar_products,
        'reviews_count': reviews.count(),
    })


#@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Проверка прав доступа
    if not request.user.is_staff:
        return redirect('home')  # Перенаправление на главную страницу

    product.delete()
    return redirect('home')


#@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Логика добавления товара в избранное (например, через ManyToManyField)
    # Здесь предполагается, что у модели User есть связь с избранными товарами

    return redirect('product_detail', product_id=product.id)

# blog/views.py
from django.shortcuts import render
from .models import Post  # Импортируйте модель Post

def post_list(request):
    posts = Post.objects.all()  # Получаем все посты
    return render(request, 'blog/post/list.html', {'posts': posts})