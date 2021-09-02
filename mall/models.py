from django.db import models
from django.utils.text import slugify
from django.conf import settings
User = settings.AUTH_USER_MODEL

        
class Category(models.Model):
    cat_id = models.AutoField
    cat_name = models.CharField(max_length=200)
    cat_slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.cat_name
    
    def save(self, *args, **kwargs):
        self.cat_slug = self.cat_slug or slugify(self.cat_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
class SubCategory(models.Model):
    subcat_id = models.AutoField
    subcat_cat = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    subcat_name = models.CharField(max_length=200)
    subcat_slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.subcat_name

    def save(self, *args, **kwargs):
        self.subcat_slug = self.subcat_slug or slugify(self.subcat_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'sub-category'
        verbose_name_plural = 'sub-categories'

class Product(models.Model):
    
    product_id = models.AutoField
    product_name = models.CharField(max_length=200)
    product_slug = models.SlugField(unique=True, null=True, blank=True)
    product_desc = models.TextField()
    product_cat = models.ForeignKey(to=Category, related_name='products', on_delete=models.CASCADE)
    product_subcat = models.ForeignKey(to=SubCategory, related_name='products', on_delete=models.CASCADE)
    product_img = models.ImageField(upload_to="mall/images", default="")
    product_mrp = models.IntegerField()
    product_price = models.IntegerField()
    product_quantity = models.IntegerField(default=0)
    product_pub_time = models.DateTimeField()

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.product_slug = self.product_slug or slugify(self.product_name)
        super().save(*args, **kwargs)

class Cart(models.Model):
    cart_id = models.AutoField
    cart_product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    cart_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    cart_product_quantity = models.IntegerField()

    # def __str__(self):
    #     return self.cart_user
    
class Order(models.Model):
    order_status_choices = (
        ('Requested', 'Requested'),
        ('Accepted', 'Accepted'),
        ('Payment Success', 'Payment Success'),
        ('Payment Failed', 'Payment Failed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
        ('Refunded', 'Refunded')
    )
    order_id = models.CharField(max_length=25)
    item_id = models.AutoField
    order_products = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    order_user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=80)
    mobile = models.CharField(max_length=14)
    amount = models.IntegerField(default=0)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    prod_quantity = models.IntegerField()
    order_status = models.CharField(max_length=256, choices=order_status_choices, default="Requested")
    orderTime = models.DateTimeField()

    def __str__(self):
        return self.user_name


