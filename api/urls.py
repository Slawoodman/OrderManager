from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("", views.getRoutes),
    path("products/", views.getProducts),
    path("products/<str:pk>", views.getProduct),
    path("products/<str:pk>/order/create/", views.createOrder),
    path("orders/", views.getOrders),
    path("orders/<str:pk>", views.getOrder),
    path("orders/<str:pk>/payment", views.orderPayment),
    path("orders/<str:pk>/payment/check", views.orderGenBill),
    path("orders/<str:pk>/changestatus", views.changeOrderStatus),
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
