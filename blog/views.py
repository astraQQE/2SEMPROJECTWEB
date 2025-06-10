from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review, Advertisement,Category,User,Order, OrderProduct
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import RegisterForm, ProductForm



def home(request):
    # 1. Популярные товары (используется filter() и order_by())
    popular_products = Product.objects.filter(stock__gt=0).order_by('-created')

    # 2. Последние обзоры (используется order_by())
    latest_reviews = Review.objects.order_by('-created_at')[:3]

    # 3. Активные акции (используется filter())
    active_ads = Advertisement.objects.filter(status='active')

    # 4. Товары с максимальным рейтингом (агрегатная функция Avg)
    top_rated_products = Product.objects.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=4.5).order_by('-avg_rating')[:3]

    products_with_multiple_in_category = Product.objects.annotate(category_product_count=Count('category__product')).filter(category_product_count__gt=1)




    print("Products with multiple in category:", list(products_with_multiple_in_category))

    return render(request, 'blog/index.html', {
        'popular_products': popular_products,
        'latest_reviews': latest_reviews,
        'active_ads': active_ads,
        'top_rated_products': top_rated_products,
        'products_with_multiple_in_category': products_with_multiple_in_category,
    })





def search(request):
    query = request.GET.get('q')
    results = []
    if query:
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




@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user  # Привязываем товар к текущему пользователю
            product.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()

    return render(request, 'blog/add_product.html', {'form': form})

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
        form = RegisterForm(request.POST)
        print("FORM IS VALID:", form.is_valid())  # Отладочная информация
        if form.is_valid():
            user = form.save()
            print("USER CREATED:", user)  # Отладочная информация

            # Определяем роль пользователя
            role = form.cleaned_data['role']
            group_name = 'buyers' if role == 'buyer' else 'admins'
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            # Автоматический вход после регистрации
            login(request, user)

            return redirect('home')
    else:
        form = RegisterForm()

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


def product_delete(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('home')


def product_edit(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'blog/product_edit.html', {'form': form,'product': product})
#@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)


    return redirect('product_detail', product_id=product.id)

# blog/views.py
from django.shortcuts import render
from .models import Post  # Импортируйте модель Post

def post_list(request):
    posts = Post.objects.all()  # Получаем все посты
    return render(request, 'blog/post/list.html', {'posts': posts})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get('cart_id')

    if not cart_id:
        # Создаем новый заказ (корзину) для гостя
        order = Order.objects.create(status='pending', total_amount=0)  # Указываем дефолтное значение
        request.session['cart_id'] = order.id  # Сохраняем ID корзины в сессии
    else:
        # Используем существующую корзину
        order = Order.objects.get(id=cart_id)

    # Добавляем товар в корзину
    order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
    if not created:
        order_product.quantity += 1
        order_product.save()

    # Обновляем общую сумму заказа
    order.total_amount = sum(op.product.price * op.quantity for op in order.orderproduct_set.all())
    order.save()

    return redirect('cart_view')

def remove_from_cart(request, product_id):
    """Удаление товара из корзины."""
    product = get_object_or_404(Product, id=product_id)
    cart_id = request.session.get('cart_id')

    if cart_id:
        order = Order.objects.get(id=cart_id)
        order_product = OrderProduct.objects.filter(order=order, product=product).first()
        if order_product:
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order_product.delete()

    return redirect('cart_view')

def cart_view(request):
    """Просмотр корзины."""
    cart_id = request.session.get('cart_id')
    if cart_id:
        order = Order.objects.get(id=cart_id)
        order_products = order.orderproduct_set.all()
    else:
        order_products = []

    return render(request, 'blog/cart.html', {'order_products': order_products})