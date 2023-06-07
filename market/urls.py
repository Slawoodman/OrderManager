from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.mainpage, name="main"),
    path("order/<str:pk>", views.createUserOrder, name="user-order"),
    path("orders/", views.filter_orders, name="showorders"),
    path("checkout/<int:pk>", views.mark_order_item_as_paid, name="checkout"),
    path("payment/<int:pk>", views.generate_payment_html, name="genpayment"),
    path("download_file/<int:pk>", views.download_file, name="view_html"),
    path(
        "orders/<int:pk>/change_status/",
        views.change_order_status,
        name="change_order_status",
    ),
]
