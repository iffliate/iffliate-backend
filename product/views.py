from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,viewsets,mixins
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from .serializer import (ProductSerializer, OrderSerializer,UserOrderCleanerSerializer,
OrderHistoryCleanSerializer,OrderHistoryShopManageSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Product, Order,OrderHistory
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
    filterset_class = custom_filters.ProductFilter
    search_fields = [
        'orderId',
        'status'
    ]
    filterset_fields = [
        'orderId',
        'status'
    ]  
    def get(self,request):
        queryset =Order.objects.all()
        serialized = UserOrderCleanerSerializer(self.filter_queryset(queryset),many=True,context={'request':request})
        return Success_response(msg="Success",data=serialized.data,status_code =status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            order = serializer.save(user=request.user)
            clean_data = UserOrderCleanerSerializer(order,many=False,context={'request':request})
            return Success_response(msg="Created",data=clean_data.data,status_code =status.HTTP_201_CREATED)

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
            




class UserOrderManagemnt(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset  = OrderHistory.objects.all()
    filterset_class = custom_filters.OrderHistoryFiter
    serializer_class = OrderHistoryCleanSerializer
    permission_classes = [IsAuthenticated]


    @action(detail=False,methods=['get'])
    def get_all_paystack_keys(self,request,pk=None):
        'we getting all the keys that will be represented as payment id'

        paystack_keys = OrderHistory.objects.filter(user=request.user.id).values('paystack').distinct()

        return Success_response(msg="Success",data=paystack_keys,status_code =status.HTTP_200_OK)


    def retrieve(self, request, *args, **kwargs):
        paystack_key = kwargs.get('pk',None)
        if paystack_key is None:raise CustomError(message='look up field must not be None') 
        
        get_orders_info = self.filter_queryset(self.queryset.filter(paystack=paystack_key))
        clean_data = self.serializer_class(get_orders_info,many=True)

        return Success_response(msg="Success",data=clean_data.data,status_code =status.HTTP_200_OK)

class ShopOrderManagement(mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset  = OrderHistory.objects.all()
    filterset_class = custom_filters.OrderHistoryFiter
    serializer_class = OrderHistoryCleanSerializer
    permission_classes = [IsAuthenticated , IsShopOwner]


    @action(detail=True,methods=['get'])
    def get_all_paystack_keys(self,request,pk=None):
        'we getting all the keys that will be represented as payment id for the shop'
        paystack_keys = OrderHistory.objects.filter(shop=pk).values('paystack').distinct()
        return Success_response(msg="Success",data=paystack_keys,status_code =status.HTTP_200_OK)



    def retrieve(self, request, *args, **kwargs):
        'get all product that the users has bought from ur store'
        paystack_key = kwargs.get('pk',None)
        if paystack_key is None:raise CustomError(message='look up field must not be None') 
        
        get_orders_info = self.filter_queryset(self.queryset.filter(paystack=paystack_key))
        clean_data = self.serializer_class(get_orders_info,many=True)

        return Success_response(msg="Success",data=clean_data.data,status_code =status.HTTP_200_OK)

    

    def create(self, request, *args, **kwargs):
        serilized = OrderHistoryShopManageSerializer(data=request.data)
        serilized.is_valid(raise_exception=True)
        data = serilized.save()

        clean_data = self.serializer_class(data,many=True)
         
        return Success_response(msg='Updated',data=clean_data.data,status_code=status.HTTP_200_OK)