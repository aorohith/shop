from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django.urls import reverse

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','brand','category','product_image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','customer_info','product','product_info','quantity','ordered_date','status']

    # link creation function to view details of customer in admin panel
    def customer_info(self,obj):
        link = reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)

    # link creation function to view details of products in admin panel
    def product_info(self,obj):
        link = reverse('admin:app_product_change',args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
