from django.db import models
from django.contrib.auth.models import User
from django_rest_passwordreset.tokens import get_token_generator


STATUS_CHOICES = (
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)


class Shop(models.Model):
    """Модель магазина"""
    objects = models.manager.Manager()

    name = models.CharField(max_length=50, verbose_name='Название магазина')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Статус получения заказов', default=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Магазины"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории"""
    objects = models.manager.Manager()

    name = models.CharField(max_length=50, verbose_name='Название категории')
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории товаров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""
    objects = models.manager.Manager()

    name = models.CharField(max_length=100, verbose_name='Название продукта')
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = "Продукты"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    """Модель информации о продукте"""
    objects = models.manager.Manager()

    model = models.CharField(max_length=80, verbose_name='Модель', blank=True)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД', unique=True)
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='product_infos', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='product_infos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = "Информация о продуктах"

    def __str__(self):
        return self.model


class Parameter(models.Model):
    """Модель имени параметра"""
    objects = models.manager.Manager()

    name = models.CharField(max_length=50, verbose_name='Название параметра')

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Параметры продуктов"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    """Модель параметра продукта"""
    objects = models.manager.Manager()

    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте',
                                     related_name='product_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters',
                                  on_delete=models.CASCADE)
    value = models.CharField(verbose_name='Значение', max_length=100)

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = "Список параметров продуктов"
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
        ]

    def __str__(self):
        return f'{self.product_info} - {self.parameter}'


class Order(models.Model):
    """Модель заказа"""
    objects = models.manager.Manager()

    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='orders', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', choices=STATUS_CHOICES, max_length=15)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"
        ordering = ('-dt',)

    def __str__(self):
        return f'{str(self.id)} - {self.status}'


class OrderItem(models.Model):
    """Модель позиции заказа"""
    objects = models.manager.Manager()

    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте', related_name='order_items', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Список заказанных позиций"

    def __str__(self):
        return f'{self.order} - {self.product}'


class Profile(models.Model):
    """Модель профиля пользователя"""
    objects = models.manager.Manager()

    user = models.OneToOneField(User, verbose_name='Пользователь', related_name='profile', on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом')
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = "Профили пользователей"


class ConfirmEmailToken(models.Model):
    """Модель токена подтверждения электронной почты"""
    objects = models.manager.Manager()

    class Meta:
        verbose_name = 'Токен подтверждения Email'
        verbose_name_plural = 'Токены подтверждения Email'

    @staticmethod
    def generate_key():
        """Генерирует псевдослучайный код с помощью os.urandom и binascii.hexlify"""
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name='confirm_email_tokens',
        on_delete=models.CASCADE,
        verbose_name="Пользователь, связанный с этим токеном сброса пароля"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Когда был сгенерирован этот токен")

    key = models.CharField('Ключ', max_length=64, db_index=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return f"Токен сброса пароля для пользователя {self.user}"
