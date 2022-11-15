from django.db import models
from authentication.models import Shop
# class Banks(models.Model):
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=20)
#     bank_type = models.CharField(max_length=20)
#     slug = models.CharField(max_length=30)
    
#     def __str__(self):
#         return self.name


class ShopWithdrawHistory(models.Model):
    recipient_code = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,null=True,default=True)
    '''
    If there is an error with the transfer request, 
    kindly retry the transaction with the same reference in order to avoid double crediting.
    If a new reference is used, the transfer would be treated as a new request.
    '''
    reference = models.TextField(default='')
    transfer_state_choice = (
        ('success','success'),
        ('failed','failed'),
        ('reversed','reversed'),
        ('pending','pending'),
    )
    transfer_state = models.CharField(choices=transfer_state_choice,max_length=15,default='pending')


    # def __str__(self) -> str:return f'{self.transfer_state} {self.shop.name}'