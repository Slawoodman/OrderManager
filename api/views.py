from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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



@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "/api/products"},
        {"GET": "/api/orders"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]
    return Response(routes)


@api_view(["GET"])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrders(request):
    user = request.user
    orders = filter_orders_by_role(user)
    serializer = OrderItemSerializer(orders, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getOrder(request, pk):
    orders = OrderItem.objects.get(id=pk)
    serializer = OrderItemSerializer(orders, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createOrder(request, pk):
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def orderPayment(request, pk):
    order_item = get_object_or_404(OrderItem, id=pk)
    user = request.user
    role = user.role

    if role == User.Role.USER and order_item.customer == user:
        try:
            order_item.paid()
            return Response("U've paid for the order.", status=status.HTTP_200_OK)
        except:
            return Response("An error occurred.", status=status.HTTP_400_BAD_REQUES)
    return Response(
        "Only owners can pay for the order.", status=status.HTTP_403_FORBIDDEN
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def orderGenBill(request, pk):
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
            "Wait for the user to pay for the order.", status=status.HTTP_400_BAD_REQUES
        )

    return Response("U shall not pass!!!", status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def changeOrderStatus(request, pk):
    order = get_object_or_404(OrderItem, id=pk)
    status = request.data.get("status")
    if status in dict(OrderItem.STATUS_CHOICES):
        order.status = status
        order.save()
        return Response("Order status changed successfully!")
    return Response("Invalid status value.")