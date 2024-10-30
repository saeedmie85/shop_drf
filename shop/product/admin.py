from django.contrib import admin
from .models import (ProductAttribute, ProductEntity, ProductValue)
# Register your models here.

@admin.register(ProductEntity)
class ProductEntityAdmin(admin.ModelAdmin):
    list_display = ['product_type','image']

@admin.register(ProductAttribute)
class ProductAttributeyAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ProductValue)
class ProductValueAdmin(admin.ModelAdmin):
    list_display = ['entity','attribute','value',]