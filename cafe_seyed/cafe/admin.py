from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = []


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = []


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_id']


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['text']
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'description','image']