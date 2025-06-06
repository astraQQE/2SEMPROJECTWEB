from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='posts')
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
class User(AbstractUser):
    ROLE_CHOICES = [
        ('buyer', _('Покупатель')),
        ('admin', _('Администратор')),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer', verbose_name=_('Роль'))
    date_registered = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата регистрации'))
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('Группы'),
        blank=True,
        related_name='blog_users'  # Избегаем конфликта с auth.User
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('Права пользователя'),
        blank=True,
        related_name='blog_users_permissions'  # Избегаем конфликта с auth.User
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название категории'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название бренда'))
    description = models.TextField(blank=True, verbose_name=_('Описание'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Бренд')
        verbose_name_plural = _('Бренды')

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Название товара'))
    description = models.TextField(verbose_name=_('Описание'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Категория'))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_('Бренд'))
    stock = models.IntegerField(verbose_name=_('Количество на складе'))
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name=_('Изображение'))
    created = models.DateTimeField(auto_now_add=True)  # Добавляем поле created


    def average_rating(self):
        """Подсчитывает средний рейтинг товара."""
        reviews = self.review_set.all()
        if reviews.exists():
            return reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
        return 0

    def __str__(self):
        return f"{self.name} ({self.brand})"

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')

class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )

    def __str__(self):
        return self.title
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('В обработке')),
        ('shipped', _('Отправлен')),
        ('delivered', _('Доставлен')),
        ('canceled', _('Отменен')),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Общая сумма'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Статус'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата изменения'))

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Заказ'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Товар'))
    quantity = models.IntegerField(default=1, verbose_name=_('Количество'))

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в заказе #{self.order.id}"

    class Meta:
        verbose_name = _('Товар в заказе')
        verbose_name_plural = _('Товары в заказах')

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Товар'))
    text = models.TextField(verbose_name=_('Текст отзыва'))
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name=_('Рейтинг'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')