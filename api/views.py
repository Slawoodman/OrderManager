from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework import status
from .serializers import ProductSerializer, OrderItemSerializer

from market.models import Product, OrderItem
from market.forms import OrderCreatForm
from users.models import User
from .utils import filter_orders_by_role



class RoutesAPIView(APIView):
    def get(self, request):
        routes = [
            {"GET": "/api/routes/"},
            {"GET": "/api/products/"},
            {"GET": "/api/products/<int:pk>/"},
            {"GET": "/api/orders/"},
            {"GET": "/api/orders/<int:pk>/"},
            {"POST": "/api/products/<int:pk>/order/create/"},
            {"POST": "/api/orders/<int:pk>/payment/"},
            {"POST": "/api/orders/<int:pk>/gen-bill/"},
            {"POST": "/api/orders/<int:pk>/change-status/"},
            {"POST": "/api/users/token/"},
            {"POST": "/api/users/token/refresh/"},

        ]
        return Response(routes)


class ProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductAPIView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)


class OrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = filter_orders_by_role(user)
        serializer = OrderItemSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data)


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = OrderItem.objects.get(id=pk)
        serializer = OrderItemSerializer(order, many=False)
        return Response(serializer.data)


class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        role = user.role
        item = Product.objects.get(id=pk)

        if role == User.Role.USER:
            form = OrderCreatForm(request.data)

            if form.is_valid():
                new_order = form.save(commit=False)
                new_order.customer = user
                new_order.product = item
                new_order.save()

                return Response(
                    "New order created successfully!", status=status.HTTP_201_CREATED
                )
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "Only users can create a new order.", status=status.HTTP_403_FORBIDDEN
            )


class OrderPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order_item = get_object_or_404(OrderItem, id=pk)
        user = request.user
        role = user.role

        if role == User.Role.USER and order_item.customer == user:
            try:
                order_item.paid()
                return Response("U've paid for the order.", status=status.HTTP_200_OK)
            except:
                return Response("An error occurred.", status=status.HTTP_400_BAD_REQUEST)
        return Response(
            "Only owners can pay for the order.", status=status.HTTP_403_FORBIDDEN
        )


class OrderGenBillAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order_item = get_object_or_404(OrderItem, id=pk)
        user = request.user

        if request.user.role == User.Role.CASHIER:
            if order_item.is_paid:
                file_name = "payment.html"
                context = {
                    "order_item": order_item,
                }
                html_content = render_to_string("market/payment_template.html", context)

                # Save the HTML content to the OrderItem instance
                order_item.file.save(file_name, ContentFile(html_content), save=True)
                return Response("Payment is created...", status=status.HTTP_200_OK)
            return Response(
                "Wait for the user to pay for the order.", status=status.HTTP_400_BAD_REQUEST
            )

        return Response("U shall not pass!!!", status=status.HTTP_403_FORBIDDEN)


class ChangeOrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(OrderItem, id=pk)
        status = request.data.get("status")
        if status in dict(OrderItem.STATUS_CHOICES):
            order.status = status
            order.save()
            return Response("Order status changed successfully!")
        return Response("Invalid status value.")