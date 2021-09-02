from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from .models import Product, Category, SubCategory, Cart, Order
from django.template.defaultfilters import truncatechars

# Register your models here.
admin.site.site_header = "Thole Mall - Admin"


# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'cat_slug': ('cat_name',)
    }

# admin.site.register(SubCategory)
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    def Sub_Category(self):
        return self.subcat_name
    def category(self):
        return self.subcat_cat
    list_display = [
        Sub_Category,
        category
    ]
    prepopulated_fields = {
        'subcat_slug': ('subcat_name',)
    }

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product_name', 'product_cat', 'product_subcat', 'product_price', 'id']
    def Product_name(self):
        return truncatechars(self.product_name, 50)
    list_display = [
        Product_name,
        'product_cat',
        'product_subcat',
        'product_quantity'
    ]
    prepopulated_fields = {
        'product_slug': ('product_name',)
    }

# admin.site.register(Cart)
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    def product(self):
        return truncatechars(self.cart_product, 35)
    search_fields=(
        'cart_id',
        'cart_user',
        'cart_product',
        'cart_prod_quantity'
    )
    list_display=(
        'id',
        'cart_user',
        product,
        'cart_product_quantity'
    )

# admin.site.register(Order)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields=(
        'order_id',
        'id',
        'user_name',
        'city'
    )
    def product(self):
        return truncatechars(self.order_products, 35)
    list_display=(
        'order_id',
        'id',
        'user_name',
        product,
        'mobile',
        'city',
        'state',
        'pincode',
        'order_status'
    )




# admin.site.unregister(Group)
