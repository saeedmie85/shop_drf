from django.urls import path, include
from .views import UserRegistrationView, UserVerifyView, LoginView, logoutView

app_name = "accounts"

urlpatterns = [
    path("api/v1/", include("accounts.api.v1.urls")),
]
