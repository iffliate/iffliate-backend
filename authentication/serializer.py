from venv import create
from rest_framework import serializers
from .models import Shop
from django.template.defaultfilters import slugify

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        exclude = ['slug', 'user']
        
    def create(self, validated_data):
        slug = slugify(validated_data["name"])
        return Shop.objects.create(slug=slug, **validated_data)
        