import django_filters
from . import models


class ShopFilter(django_filters.FilterSet):

    user = django_filters.NumberFilter(field_name='user__id')
    class Meta:
        model = models.Shop
        fields = ['user']