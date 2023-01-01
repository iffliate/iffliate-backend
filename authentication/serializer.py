from venv import create
from utils.custom_response import CustomError
from rest_framework import serializers
from .models import Shop,User
from product import models as product_models,serializer as product_serialzer
from django.template.defaultfilters import slugify


class UserCreateSerializer(serializers.ModelSerializer):
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise CustomError({'error':'email already exist'})
        return super().validate(attrs)

    def create(self, validated_data):
        user  = User.objects.create_user(
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            **validated_data
        )
        return user
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        # exclude = [ 'user']
        fields = ['user',
        'id','name','slug','facebook','twitter','whatsapp','instagram','about','banner','logo','info',
        'account_holder_name','account_number','account_holder_email','bank_name','address_country','address_city',
        'address_zip','street_address','created_at','updated_at','wallet','phone','phone_number'
        ]
        extra_kwargs = {'user': {'read_only': True}}
        
    def create(self, validated_data):
        slug = slugify(validated_data["name"]+str(Shop.objects.count()))
        return Shop.objects.create(slug=slug, **validated_data)


    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     return dict()
class ShopRelatedProduct(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()


    class Meta:
        model = Shop
        fields = [ 
            'name','id','facebook','twitter','whatsapp','instagram',
            'about','banner','logo','info','products','user','phone','address_country','address_city','street_address',
            'address_zip','phone_number'
        ]

    def get_products(self,shop):
        products =product_models.Product.objects.filter(shop=shop)

        cleaner = product_serialzer.ProductSerializer(products,many=True)

        return cleaner.data
    