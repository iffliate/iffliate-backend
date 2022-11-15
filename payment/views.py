from django.http import HttpResponse
from django.shortcuts import render
import requests,json
from utils.extraFunc import convert_naira_to_kobo,get_amount_by_percent
from utils.custom_response import CustomError, Success_response
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status,authentication,permissions
from product import models as product_app_models
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.auth import get_user_model
from authentication import models as auth_models
from django.core.files.base import ContentFile
from product import models as product_models
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from . import serializer
from authentication.models import Shop
from product.permission import IsShopOwner
from .models import ShopWithdrawHistory
# from .models import Banks
# from .serializer import BankSerializer
# Create your views here.


def very_payment(request,reference=None):
    # this would be in the call back to check if the payment is a success
    if reference is None:
        raise CustomError({"error":"You need to send a refrence back"})
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
    'Authorization': 'Bearer '+settings.PAYSTACK_SECRET,
    'Content-Type' : 'application/json',
    'Accept': 'application/json',
    }
    try:
        resp = requests.get(url,headers=headers)
    except requests.ConnectionError:
        raise CustomError({"error":"Nework Error"}) 

    if resp.json()['data']['status'] == 'success':
        return Success_response(msg="Recived the Request Succefully",)
    raise CustomError({"error":"Something Went Wrong Try Again"},status_code=status.HTTP_400_BAD_REQUEST)

    
    



class InitPayment:
    'this class handles the initializing of payment it bassically proccess payment and sends back payment link so user can use'


    def __init__(self,email,amount,meta_data=dict()) -> None:
        self.email=email
        self.amount=amount
        self.meta_data= meta_data
        self.url = 'https://api.paystack.co/transaction/initialize/'


    def create_payment_link(self):
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET}',
            'Content-Type' : 'application/json',
            'Accept': 'application/json',}
        body = {
            "email":self.email,
            "amount": convert_naira_to_kobo(self.amount),
            "metadata":self.meta_data,}

        try:
            resp = requests.post(self.url,headers=headers,data=json.dumps(body))
        except requests.ConnectionError:
            raise CustomError({"error":"Network Error please try again in few minutes"},status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
               
        if resp.status_code ==200:
            data = resp.json()
            return data

        raise CustomError(message='Some Error Occured Please Try Again',status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        
@csrf_exempt
def payment_webhook(request,pk=None):
    "this receives Payload from paystack"
    # data = json.loads(request.body)
    data = json.loads(request.body)
    

    if data.get('event') == 'charge.success':
        meta_data =data['data']['metadata']
        "this means the payment was a success"
        if meta_data['forWhat'] =='order_payment':
            '''
            we handle the order payment
                get the amount paid
                store all info we have in the OrderHistory -- done
                iffiate get 25% -getting the percent from each OrderItem
                the shop get 75%-getting the percent from each OrderItem
                based on the 75% we credit the shop wallet
            '''
            order_id  = meta_data['order_id']
            order = product_app_models.Order.objects.get(id=order_id)
            if order.is_paid == False:
                # i noticed paystack sends a hook again resulting to to many order
                order.is_paid=True
                order.save()
                # user = get_user_model().objects.get(id=order.user.id)
                # picture_copy  =ContentFile(eachitem.image.read())
                for eachitem in product_app_models.OrderItem.objects.filter(order=order.id):
                    shop_earnings = get_amount_by_percent(75,eachitem.product.actual_price*eachitem.quantity)
                    shop =auth_models.Shop.objects.get(id= eachitem.shop.id)
                    shop.wallet = shop.wallet +shop_earnings
                    shop.save()
                    order_history =product_models.OrderHistory.objects.create(
                        shop =shop,
                        user = order.user,
                        buyer_first_name= order.user.first_name,
                        buyer_last_name = order.user.last_name,
                        buyer_email=order.user.email,
                        buyer_phone = meta_data['buyer_phone'],
                        buyer_shipping_address = meta_data['shipping_addresse'],
                        amount = eachitem.product.actual_price,
                        paystack = order.paystack,
                        quantity = eachitem.quantity,
                        product_name=eachitem.product.name,
                        description=eachitem.product.description,
                        iffiliate_earning= get_amount_by_percent(25,eachitem.product.actual_price*eachitem.quantity),
                        shop_earning=shop_earnings,

                        # image_one=eachitem.image_one,
                    
                    )


    if data.get('event') == 'transfer.success':
        recipient_code = data['data']['recipient']['recipient_code']
        shop_widthraw = ShopWithdrawHistory.objects.filter(recipient_code=recipient_code).first()
        shop_widthraw.transfer_state='success'
        shop_widthraw.save()

        'since it succefful we need to reduce the wallet'
        shop = Shop.objects.get(id=shop_widthraw.shop.id)
        shop.wallet = shop.wallet - shop_widthraw.amount
        shop.save()
    if data.get('event') == 'transfer.failed':
        recipient_code = data['data']['recipient']['recipient_code']
        shop_widthraw = ShopWithdrawHistory.objects.filter(recipient_code=recipient_code).first()
        shop_widthraw.transfer_state='failed'
        shop_widthraw.save()
    if data.get('event') == 'transfer.reversed':
        shop_widthraw = ShopWithdrawHistory.objects.filter(recipient_code=recipient_code).first()
        shop_widthraw.transfer_state='reversed'
        shop_widthraw.save()

    return HttpResponse(status.HTTP_200_OK)




class InitOrderTran(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    

    def post(self, request,order_id=None):
        extra_data = request.data
        buyer_phone = extra_data.get('phone',None)
        shipping_addresse = extra_data.get('shipping_addresse',None)

        if shipping_addresse is None:raise CustomError({'error':'please provide a shipping address'})
        if buyer_phone is None:raise CustomError({'error':'please provide a Phone Number'})

        if not product_app_models.Order.objects.filter(id=order_id,).exists():
            raise CustomError(message='Order does not exists',status_code=status.HTTP_400_BAD_REQUEST)

        order = product_app_models.Order.objects.get(id=order_id)
        if order.user.id != request.user.id:CustomError(message='Not Found',status_code=status.HTTP_400_BAD_REQUEST)
        if order.is_paid != False:CustomError(message='Not Found',status_code=status.HTTP_400_BAD_REQUEST)
        # user=request.user.id,=False
        init = InitPayment(
            email=order.user.email,
            amount=order.total_amount,
            meta_data={
                'order_id':order.id,
                'forWhat':'order_payment',
                'buyer_phone':buyer_phone,
                'shipping_addresse':shipping_addresse
            }
        )
        response = init.create_payment_link()
        order.paystack = response['data']['reference']
        order.save()
        
        
        return Success_response(msg="Created",data=response,status_code =status.HTTP_201_CREATED)













class HandleShopPaymentView(viewsets.ViewSet):
    
    serializer_class =serializer.HandleShopPaymentView
    permission_classes = [ IsShopOwner]

    def create(self, request):
        'this is what handles the users payment'
        serialized = self.serializer_class(data=request.data,many=False)
        serialized.is_valid(raise_exception=True)

        serialized.save()

        return Success_response('Workign on it',data=[],)



