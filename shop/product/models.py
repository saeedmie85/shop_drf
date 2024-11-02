from django.db import models
from django.utils.text import slugify
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from datetime import datetime
from django.dispatch.dispatcher import receiver

User = get_user_model()


def product_image(instance, filename):
    return "images/{0}.jpg".format(instance.slug)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    is_visible = models.BooleanField(default=False)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class AvailableManager(models.Manager):
    def get_queryset(self):
        return (
            super(AvailableManager, self)
            .get_queryset()
            .filter(is_available=True, quantity__gte=1)
        )


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=True)
    category = models.ManyToManyField(
        Category,
        related_name="products",
    )
    price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    objects = models.Manager()
    available = AvailableManager()
    image = models.ImageField(upload_to=product_image, null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("updated",)

    def save(self):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save()


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.product.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"{self.province}-{self.city}-{self.street}-{self.note}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    status = models.CharField(max_length=50, blank=True, default="register")
    delivery_date = models.DateTimeField(null=True, blank=True)
    tracking_code = models.CharField(max_length=20)
    total_price = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created",)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()


@receiver(post_delete, sender=Product)
def product_image_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(True)
