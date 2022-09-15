from wsgiref import validate
from .models import Order, OrderItem, Product, Images, Sizes, Category
from rest_framework import serializers
from .utils import getUniqueId
from django.template.defaultfilters import slugify

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields=[
            'product', 
            'quantity',
            'size'
        ]


        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = [
            'orderId',
            'items',
            'total_amount',
            'status'
        ]
        read_only_fields =['orderId', 'total_amount']
    
    def create(self, validated_data):
        print(validated_data)
        user = validated_data["user"]
        if not user.phone and not user.billing_address:
            raise serializers.ValidationError("User must update phone number and billing address")
        items_data = validated_data.pop('items')
        total_amount = 0
        for item_data in items_data:
            product = Product.objects.get(name=item_data["product"])
            if item_data["quantity"]:
                amount = product.slashed_price * item_data["quantity"]
            else:
                amount = product.slashed_price
            total_amount = total_amount + amount
        orderId = getUniqueId()
        order = Order.objects.create(orderId=orderId, total_amount=total_amount, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'image_one',
            'image_two',
            'image_three', 
            'image_four'
        ]

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'description',
            'slashed_price',
            'slash_percentage',
            'actual_price',
            'shop',
            'images',
            'out_of_stock'
            
        ]
        read_only_fields = ["slash_percentage", "slug"]
    
    def create(self, validated_data):
        images = validated_data.pop('images')
        slug = slugify(validated_data["name"])
        if validated_data["slashed_price"]:
            slashed_percentage = ((validated_data["actual_price"] - validated_data["slashed_price"])/validated_data["actual_price"]) * 100
            slash_percentage = int(slashed_percentage)
        else:
            slash_percentage = 0
            validated_data["slashed_price"] = validated_data["actual_price"]
        product = Product.objects.create(slug=slug, slash_percentage=slash_percentage, **validated_data)
        for image in images:
            Images.objects.create(product=product, **image) 
        return product