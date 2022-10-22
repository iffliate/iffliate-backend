import django_filters
from . import models


class ProductFilter(django_filters.FilterSet):
    shop = django_filters.NumberFilter(field_name='shop__id')
    out_of_stock=django_filters.BooleanFilter(field_name='out_of_stock')
    class Meta:
        fields = ['shop','out_of_stock']
        model = models.Product


class OrderFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='user__id')
    is_paid = django_filters.BooleanFilter(field_name='is_paid')

    class Meta:
        fields = ['is_paid','user']
        model = models.Order



class OrderHistoryFiter(django_filters.FilterSet):
    shop = django_filters.NumberFilter(field_name='shop__id')

    class Meta:
        fields = ['status','shop']
        model = models.OrderHistory