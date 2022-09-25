from django.contrib import admin
from .models import (Product, Order, OrderItem
# , Images
, Sizes, Category)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['name']}
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(Images)
admin.site.register(Sizes)
admin.site.register(Category)