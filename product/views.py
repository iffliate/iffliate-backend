import re
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializer import ProductSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Product, Order
from .permission import UpdateOrDelete

class ProductCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Product.objects.filter(out_of_stock=False)
    search_fields = [
        'name',
        'category__name'
    ]
    filterset_fields = [
        'name',
        'category__name',
    ]  
    
class OrderCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    search_fields = [
        'orderId',
        'status'
    ]
    filterset_fields = [
        'orderId',
        'status'
    ]  
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'orderId'
    queryset = Order.objects.all()
    
        
    
    
class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [UpdateOrDelete]
    lookup_field = 'slug'
    queryset = Product.objects.filter(out_of_stock = False)
            