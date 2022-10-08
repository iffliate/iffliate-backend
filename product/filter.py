import django_filters
from . import models


class ProductFilter(django_filters.FilterSet):
    shop = django_filters.NumberFilter(field_name='shop__id')
    out_of_stock=django_filters.BooleanFilter(field_name='out_of_stock')
    class Meta:
        fields = ['shop','out_of_stock']
        model = models.Product
