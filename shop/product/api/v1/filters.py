# product/filters.py
import django_filters
from product.models import Product, Order


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    is_available = django_filters.BooleanFilter(field_name="is_available")
    is_featured = django_filters.BooleanFilter(field_name="is_featured")

    class Meta:
        model = Product
        fields = ["category", "min_price", "max_price", "is_available", "is_featured"]


class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
    delivery_date = django_filters.DateFromToRangeFilter(field_name="delivery_date")

    class Meta:
        model = Order
        fields = ["status", "delivery_date"]
