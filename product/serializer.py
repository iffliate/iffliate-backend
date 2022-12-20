from re import L
from wsgiref import validate
from utils.custom_response import CustomError
from . import models as product_app_models
from authentication import models as auth_models
from authentication.models import Shop
from rest_framework import serializers
from .utils import getUniqueId
from django.template.defaultfilters import slugify
from rest_framework import status
class OrderItemsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    # shop_id = serializers.IntegerField()




        
"""THe plan is once the click on checkout on check out page
checkout model is created after computation we send back a paystack key after payment we use the webhook to see 
if the person paid or not
    if the person pay then we do calculation to credit each vendor thier money they earn 
    after Order to is paid and we close the cart
"""
class OrderSerializer(serializers.Serializer):
    items = OrderItemsSerializer(many=True)

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        """

        create a order(user) - using get_or_create
        total_amount =  a function to get total data

        for each item in order_items
            OrderItem(
                order = orderInstance,
                product= product instnce,
                quantity = quantity,
                shop = shop instance
            )
        """

        items = validated_data.get('items')
        print({'items':items})
        user = self.context.get('user')
        order,_ = product_app_models.Order.objects.get_or_create(user=user,is_paid=False)
        print(order)

        order.save()    
        for item in items:
            product = product_app_models.Product.objects.get(id=item.get('product_id'))
            # shop = auth_models.Shop.objects.get(id=product)
            'to avoid duplicate order item we just overide quantity'
            order_item,_ = product_app_models.OrderItem.objects.get_or_create(
                order=order,
                product=product,
            )
            order_item.quantity= item.get('quantity')
            order_item.shop=product.shop
            order_item.save()
        return order

class OrderItemCleaner(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self,item):
        def create_img_link(img_col):
            try:
                return img_col.url
            except:return None
        product =item.product
        data = {
            'id':product.id,
            'shop':product.shop.id,
            'category':product.category.id,
            'out_of_stock':product.out_of_stock,
            'name':product.name,
            'description':product.description,
            'slashed_price':product.slashed_price,
            'actual_price':product.actual_price,
            'slash_percentage':product.slash_percentage,
            'slash_percentage':product.slash_percentage,
            'image_one':create_img_link(product.image_one),
            'image_two':create_img_link(product.image_two),
            'image_three':create_img_link(product.image_three),
            'image_four':create_img_link(product.image_four),
        }


        return data

    class Meta:
        model  =product_app_models.OrderItem
        fields = [
            'id',
            'quantity',
            'size',
            'product'
        ]

class UserOrderCleanerSerializer(serializers.ModelSerializer):
    'helps send clean data to the fron end'
    items  = serializers.SerializerMethodField()
    user  = serializers.SerializerMethodField()
    
    
    def get_items(self,order):
        # return product_app_models.OrderItem.objects.filter(order=order.id).values(
        #   'id','product','product__name','quantity','shop','size',
        #               'product__image_two',

        # )
        data = product_app_models.OrderItem.objects.filter(order=order.id)
        clean = OrderItemCleaner(data,many=True,context={'request':self.context.get('request')})
        return clean.data
    def get_user(self,order):
        user = auth_models.User.objects.get(id=order.user.id)
        return {
            'email':user.email,
            'phone':user.phone,
            'first_name':user.first_name,
            'last_name':user.last_name
        }
    class Meta:
        model = product_app_models.Order
        fields  = [
            'id',
            'user',
            'created_at',
            'is_paid','total_amount','items'
        ]

class ProductSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True)
    class Meta:
        model = product_app_models.Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'slashed_price',
            'slash_percentage',
            'actual_price',
            'shop',
            'category',
            # 'images',
            'out_of_stock',
            'image_one',
            'image_two',
            'image_three',
            'image_four',

            
        ]
        read_only_fields = ["slash_percentage", "slug",]
    
    def create(self, validated_data):
        # images = validated_data.pop('images')
        request = self.context.get('request')
        if not self.check_if_shop_owner(request,validated_data):
            raise CustomError({'shop':'You not the shop owner'},status_code=status.HTTP_401_UNAUTHORIZED)
        slug = slugify(validated_data["name"])
        if validated_data["slashed_price"]:
            slashed_percentage = ((validated_data["actual_price"] - validated_data["slashed_price"])/validated_data["actual_price"]) * 100
            slash_percentage = int(slashed_percentage)
        else:
            slash_percentage = 0
            validated_data["slashed_price"] = validated_data["actual_price"]
        category = product_app_models.Category.objects.get(id=validated_data['category'].id)
        if category.name.lower() in ['bakery','food']:
            pass
        else:
            validated_data["actual_price"]  = validated_data["actual_price"]  + 3000
        product = product_app_models.Product.objects.create(slug=slug, slash_percentage=slash_percentage, **validated_data)
        # for image in images:
        #     Images.objects.create(product=product, **image) 
        return product
    
    def check_if_shop_owner(self,request,validated_data):
        current_shop =validated_data.get('shop',)
        
        return request.user.id == current_shop.user.id

class CategorySerailizer(serializers.ModelSerializer):
    
    class Meta:
        model = product_app_models.Category
        fields = [ 'id','name']

class OrderHistoryCleanSerializer(serializers.ModelSerializer):

    class Meta:
        model = product_app_models.OrderHistory
        fields = '__all__'


class OrderHistoryShopManageSerializer(serializers.Serializer):
    paystack =serializers.CharField()
    status = serializers.CharField()

    def validate(self, attrs):
        if not product_app_models.OrderHistory.objects.filter(paystack = attrs.get('paystack')).exists():
            raise CustomError({'error':'order historys does not exists'})
        return super().validate(attrs)

    def create(self, validated_data):
        paystack = validated_data.get('paystack')
        status = validated_data.get('status')
        product_app_models.OrderHistory.objects.filter(paystack=paystack).update(status=status)

        return product_app_models.OrderHistory.objects.filter(paystack=paystack)