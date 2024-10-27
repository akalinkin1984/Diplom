from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)


class Shop(models.Model):
    """Модель магазина"""
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField()

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(max_length=50, verbose_name='Название')
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=100, verbose_name='Название')
    categoty = models.ForeignKey(Category, verbose_name='Категория', related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    """Модель информации о продукте"""
    name = models.CharField(max_length=100, verbose_name='Название')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='product_infos', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='product_infos', on_delete=models.CASCADE)


class Parameter(models.Model):
    """Модель имени параметра"""
    name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    """Модель параметра продукта"""
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте', related_name='product_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)


class Order(models.Model):
    """Модель заказа"""
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='orders', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', choices=STATUS_CHOICES, max_length=15)

    def __str__(self):
        return f'{str(self.dt)} {self.status}'


class OrderItem(models.Model):
    """Модель позиции заказа"""
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='order_items', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')


class Contact(models.Model):
    """Модель контактов"""
    type = models.CharField(verbose_name='Тип контакта', max_length=20)
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='contacts', on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)
