from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"cart-items", views.CartItemViewSet)
router.register(r"addresses", views.AddressViewSet)
router.register(r"orders", views.OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
