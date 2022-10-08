import re
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializer import ProductSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Product, Order
from .permission import UpdateOrDelete,IsShopOwner
from utils.custom_response import CustomError, Success_response
from rest_framework import status
from utils.custom_parsers import NestedMultipartParser
from rest_framework.parsers import  FormParser
from . import filter as custom_filters

class ProductCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsShopOwner]
    queryset = Product.objects.all()
    parser_classes = (NestedMultipartParser,FormParser,)
    filterset_class = custom_filters.ProductFilter
    
    # search_fields = [
    #     'name',
    #     'category__name',''
    # ]
    # filterset_fields = [
    #     'name',
    #     'category__name',
    # ]  

    def get(self,request):
        serialized = self.serializer_class(self.filter_queryset(self.queryset),many=True)
        return Success_response(msg="Success",data=serialized.data,status_code =status.HTTP_200_OK)

    def post(self,request):
        serialized = self.serializer_class(data=request.data,context={'request':request})
        serialized.is_valid(raise_exception=True)
        Instance = serialized.save()

        clean_data  = self.serializer_class(Instance,many=False)
        return Success_response(msg="Created",data=clean_data.data,status_code=status.HTTP_201_CREATED)

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
    def get(self,request):
        serialized = self.serializer_class(self.queryset,many=True)
        return Success_response(msg="Success",data=serialized.data,status =status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Success_response(msg="Created",data=serializer.data,status =status.HTTP_201_CREATED)

        # return Response(, status=)
        raise CustomError(message=serializer.errors,status_code=status.HTTP_400_BAD_REQUEST)


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
            