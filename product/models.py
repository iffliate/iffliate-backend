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

    "this will just be for easy refrence"
    shop = models.ForeignKey(Shop,on_delete=models.SET_NULL,null=True)  

class OrderHistory(models.Model):
    'this stores the orders that the user has bought with money successfully'
    # the  foreignKey is so the shop and user can access the info
    created_at = models.DateTimeField(auto_now_add=True)
    
    shop = models.ForeignKey(Shop,on_delete=models.SET_NULL,null=True)  
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    # buyer info is for shop owner if the user has been deleted they will still be able to access the buyer info
    buyer_first_name = models.CharField(max_length=255,default='')
    buyer_last_name = models.CharField(max_length=255,default='')
    buyer_email = models.EmailField(max_length=255,default='')
    buyer_phone = models.CharField(max_length=15, blank=True)
    buyer_shipping_address =models.TextField(default='nil')
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    paystack = models.TextField(default='')
    quantity = models.IntegerField(default=0,null=True)
    product_name = models.CharField(max_length=1000)
    description = models.CharField(max_length=300, blank=True)
    iffiliate_earning =  models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    shop_earning =  models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    "only vendor owners can edit the status"
    status_choices = (
        ('order_processing', 'order_processing',),
        ('ready_to_dispatch', 'ready_to_dispatch',),
        ('order_dispatched', 'order_dispatched',),
        ('delivered', 'delivered',),
    )
    status = models.CharField(max_length=50, choices=status_choices, default='order_processing')
    shopPhone_number = models.CharField(max_length=14,default='081')

    image_one = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    image_two = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    image_three = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    image_four = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    
    def __str__(self):
        return f'{self.buyer_email} buys {self.product_name} for {self.amount}'
    
    
class Sizes(models.Model):
    class Meta:
        verbose_name_plural='Sizes'
    product = models.ForeignKey(Product, related_name='size', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    def __str__(self):
        return f'{self.name}'

