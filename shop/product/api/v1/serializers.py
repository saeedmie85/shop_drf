from rest_framework import serializers
from product.models import Category, Product, CartItem, Address, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "is_visible"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "price",
            "discount",
            "is_available",
            "is_featured",
            "quantity",
            "image",
            "description",
            "created",
            "updated",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "user", "product", "quantity", "created", "updated"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "user",
            "city",
            "province",
            "street",
            "note",
            "created",
            "updated",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "address",
            "status",
            "delivery_date",
            "tracking_code",
            "total_price",
            "items",
            "created",
            "updated",
        ]
