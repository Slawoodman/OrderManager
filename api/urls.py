from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('products/', views.getProducts),
    path('products/<str:pk>', views.getProduct),

    path('orders/', views.getOrders),
    path('orders/<str:pk>', views.getOrder)
]