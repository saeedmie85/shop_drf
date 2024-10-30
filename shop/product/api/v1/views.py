from rest_framework import viewsets, permissions
from product.models import Category, Product, CartItem, Address, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartItemSerializer,
    AddressSerializer,
    OrderSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Get cart items for the user
        cart_items = CartItem.objects.filter(user=self.request.user)

        # Calculate the total price from cart items
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create the order with the calculated total price
        order = serializer.save(user=self.request.user, total_price=total_price)

        # Create OrderItems from CartItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
            )

        # Delete all cart items for the user after order creation
        cart_items.delete()
