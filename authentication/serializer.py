from venv import create
from rest_framework import serializers
from .models import Shop
from product import models as product_models,serializer as product_serialzer
from django.template.defaultfilters import slugify

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        # exclude = [ 'user']
        fields = ['user',
        'id','name','slug','facebook','twitter','whatsapp','instagram','about','banner','logo','info',
        'account_holder_name','account_number','account_holder_email','bank_name','address_country','address_city',
        'address_zip','street_address','created_at','updated_at','wallet'
        ]
        
    def create(self, validated_data):
        slug = slugify(validated_data["name"]+Shop.objects.count())
        return Shop.objects.create(slug=slug, **validated_data)



class ShopRelatedProduct(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()


    class Meta:
        model = Shop
        fields = [ 
            'name','id','facebook','twitter','whatsapp','instagram',
            'about','banner','logo','info','products','user'
        ]

    def get_products(self,shop):
        products =product_models.Product.objects.filter(shop=shop)

        cleaner = product_serialzer.ProductSerializer(products,many=True)

        return cleaner.data
    