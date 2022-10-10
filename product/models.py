from email.policy import default
from unicodedata import category
from django.db import models
from authentication.models import User, Shop

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural='Categories'
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    out_of_stock = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=300, blank=True)
    slashed_price = models.IntegerField()
    actual_price = models.IntegerField()
    slash_percentage = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    image_one = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    image_two = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    image_three = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    image_four = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):

    # orderId = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # total_amount = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    is_paid = models.BooleanField(default=False)
    paystack = models.TextField(default='',)

    def __str__(self) -> str:
        return f'Order number -> {self.id}'


    @property
    def total_amount(self):
        '''
        this propety is like a column in data base but it runs some calculation to get it value
        
        i choose this approach because product prices can change 
        '''
        items =OrderItem.objects.filter(order=self.id)
        return sum(map(self._getTotalAmout,items))

    def _getTotalAmout(self,item):
        'for each item we get the product and return the amount'
        try:
          
            return item.product.actual_price * item.quantity
        except:return 0 
# class Shop

# class Images(models.Model):
#     class Meta:
#         verbose_name = 'Image'
#         verbose_name_plural='Images'
#     product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
#     image_one = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
#     image_two = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
#     image_three = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
#     image_four = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    
#     def __str__(self):
#         return self.product.name
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,null=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    status_choices = (
        ('Order Processing', 'Order Processing',),
        ('Ready to Dispatch', 'Ready to Dispatch',),
        ('Order Dispatched', 'Order Dispatched',),
        ('Delivered', 'Delivered',),
    )
    "only vendor owners can edit the status"
    status = models.CharField(max_length=50, choices=status_choices, default='Order Processing')
    "this will just be for easy refrence"
    shop = models.ForeignKey(Shop,on_delete=models.SET_NULL,null=True)  
    
class Sizes(models.Model):
    class Meta:
        verbose_name_plural='Sizes'
    product = models.ForeignKey(Product, related_name='size', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.name}'