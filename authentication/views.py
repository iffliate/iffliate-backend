from authentication.filter import ShopFilter
from product.permission import IsShopOwner
from utils.custom_response import Success_response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,RetrieveAPIView
from .serializer import ShopRelatedProduct, ShopSerializer
from rest_framework.parsers import  FormParser
from utils.custom_parsers import NestedMultipartParser
from rest_framework.permissions import IsAuthenticated
from .models import Shop
from django.shortcuts import get_object_or_404
# from payment.models import Banks
import requests, json
from utils.custom_response import CustomError
from django.conf import settings

class ShopCreate(ListCreateAPIView,RetrieveAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (NestedMultipartParser,FormParser,)
    queryset = Shop.objects.all()  
    filterset_class=ShopFilter
    lookup_field = 'slug'
        
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ShopUpdate(RetrieveUpdateDestroyAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated,IsShopOwner]
    lookup_field = 'slug'
    queryset = Shop.objects.all()
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop,slug=kwargs.get('slug',None))
        serializer = ShopRelatedProduct(shop,many=False)
        return Success_response(msg='Success',data=serializer.data,status_code=status.HTTP_200_OK)  
