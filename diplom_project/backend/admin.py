from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from backend.models import (Shop, Category, Product, ProductInfo, Parameter, ProductParameter,
                            Order, OrderItem, Profile, ConfirmEmailToken)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'user', 'status', ]
    list_filter = ['status', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',  ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', ]
    list_filter = ['category__name', ]


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'external_id', 'quantity', 'price', 'price_rrc', 'product', 'shop', ]
    list_filter = ['product__name', 'shop__name', ]


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_info', 'parameter', 'value', ]
    list_filter = ['parameter__name', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dt', 'status', ]
    list_filter = ['user', 'dt', 'status', ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'shop', 'quantity', ]
    list_filter = ['order__dt', ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'city', 'phone', ]
    list_filter = ['type', 'city', ]


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'key', 'created_at', ]
