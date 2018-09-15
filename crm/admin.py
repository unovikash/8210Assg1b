from django.contrib import admin
from .models import Customer, Service, Product

# Register your models here.
class CustomerList(admin.ModelAdmin):
    list_display = ('customer_name', 'organization', 'phone')
    list_filter = ('customer_name', 'organization')
    search_fields = ('customer_name',)
    ordering = ['customer_name']

class ServiceList(admin.ModelAdmin):
    list_display = ('customer_name', 'service_category', 'setup_time')
    list_filter = ('customer_name', 'setup_time')
    search_fields = ('customer_name',)
    ordering = ['customer_name']

class ProductList(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'pickup_time')
    list_filter = ('customer_name', 'pickup_time')
    search_fields = ('customer_name',)
    ordering = ['customer_name']

admin.site.register(Customer, CustomerList)
admin.site.register(Service, ServiceList)
admin.site.register(Product, ProductList)