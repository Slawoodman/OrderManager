from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderItemSerializer
from market.models import Product, OrderItem


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/products'},
        {'GET':'/api/orders'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ] 
    return Response(routes)


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getOrders(request):
    orders = OrderItem.objects.all()
    serializer = OrderItemSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getOrder(request, pk):
    orders = OrderItem.objects.get(id=pk)
    serializer = OrderItemSerializer(orders, many=False)
    return Response(serializer.data)