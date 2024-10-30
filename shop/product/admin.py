from django.contrib import admin
from .models import Category, Product, CartItem, Address, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "is_visible"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "price",
        "discount",
        "is_available",
        "is_featured",
        "quantity",
        "updated",
    ]
    list_filter = ["is_available", "is_featured", "category"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["price", "discount", "is_available", "quantity"]
    raw_id_fields = ["category"]
    readonly_fields = ["created", "updated"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity", "created"]
    search_fields = ["user__username", "product__name"]
    list_filter = ["user", "product"]
    readonly_fields = ["created", "updated"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "province", "street", "note", "created"]
    search_fields = ["user__username", "city", "province", "street"]
    list_filter = ["province", "city"]
    readonly_fields = ["created", "updated"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "address",
        "status",
        "delivery_date",
        "tracking_code",
        "total_price",
        "created",
    ]
    search_fields = ["user__username", "tracking_code", "status"]
    list_filter = ["status", "delivery_date"]
    readonly_fields = ["created", "updated"]
    inlines = []

    def get_inlines(self, request, obj=None):
        if obj:
            return [OrderItemInline]
        return []


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ["price"]
    autocomplete_fields = ["product"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "price"]
    search_fields = ["order__user__username", "product__name"]
    list_filter = ["order", "product"]
    readonly_fields = ["order"]
