from utils.extraFunc import generate_n
from utils.custom_response import CustomError
from rest_framework import serializers
from .utils import UserPaymentPreparation
from authentication.models import Shop
from django.shortcuts import get_object_or_404
from .models import ShopWithdrawHistory
import uuid,json

# from .models import Banks

# class BankSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Banks
#         fields = '__all__'




class HandleShopPaymentView(serializers.Serializer):
    bank_name = serializers.CharField()
    account_number = serializers.CharField()
    shop_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=5, decimal_places=2)


    def validate(self, attrs):
        "validate if user actually have the amount he request it missing"
        shop_id = attrs.get('shop_id')
        amount = attrs.get('amount')
        self.validate_shop_wallet(shop_id,amount)
        return super().validate(attrs)


    def validate_shop_wallet(self, shop_id,amount):
        shop = get_object_or_404(Shop, pk=shop_id)
        if shop.wallet >= amount:pass 
        else: raise CustomError({'shop_id':'Insufficent Funds'})


    def create(self, validated_data):
        handle_payment = UserPaymentPreparation()# init class that will handle our payment process 
        bank_name = validated_data.get('bank_name')
        account_number = validated_data.get('account_number')
        shop_id = validated_data.get('shop_id')
        amount = validated_data.get('amount')
        bank_code =  handle_payment.get_bank_code(bank_name)


        test_bank = handle_payment.test_user_account(accountNumber=account_number,Bankname=bank_name,bankCode=bank_code)

        if test_bank.get('status'):
            'the bank info is good we need to start the process fast'
            recipient_code = test_bank.get('data').get('recipient_code')
            shop = Shop.objects.get(id=shop_id)
            shopwithdraw,created = ShopWithdrawHistory.objects.get_or_create(recipient_code=recipient_code,)
            if created == False and shopwithdraw.transfer_state == 'pending':
                raise CustomError({'shop_id':'We are still processing your withdrawal'})
            else:
                shopwithdraw.transfer_state = 'pending'
                shopwithdraw.shop = shop
                reference =  generate_n()
                shopwithdraw.reference=reference
                shopwithdraw.amount = amount
                shopwithdraw.save()
                metadata ={'shop_id':shop_id}
                resp = handle_payment.transfer_money(amount=amount,reference=reference,recipient=recipient_code,metadata=metadata)
                if resp.get('status') == True:
                    return resp
                else:
                    shopwithdraw.delete()
                    raise CustomError({'shop_id':resp.get('message')})
        else:
            raise CustomError({'error':test_bank.get('message')})

    

class HandleShopPaymentCleaner(serializers.ModelSerializer):


    class Meta:
        model =ShopWithdrawHistory
        fields = [ 'shop__name','amount','transfer_state','created_at']