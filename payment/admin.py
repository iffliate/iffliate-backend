from django.contrib import admin
from product import models
from .models import ShopWithdrawHistory
# from .models import Banks
# Register your models here.






admin.site.register(ShopWithdrawHistory)
admin.site.register(models.OrderHistory)
# admin.site.register(Banks)